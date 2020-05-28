import threading
import pathlib
from cli import CommandLineInterface
from utils.listener import Listener
from thought import Thought
from protocol import Hello, Config, Snapshot
from PIL import Image
import cortex_pb2
import json
import pika
from multiprocessing import Process
import cortex_pb2

cli = CommandLineInterface()

class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir, publish):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def save_color_image(self, hello, snapshot):
        with open(self.data_dir + '/' + \
            str(hello.user_id) + '_' + \
            str(snapshot.timestamp) + '_color.json', 'wb') as writer:
            writer.write(snapshot.color_image.SerializeToString())

    def save_depth_image(self, hello, snapshot):
        with open(self.data_dir + '/' + \
            str(hello.user_id) + '_' + \
            str(snapshot.timestamp) + '_depth.json', 'wb') as writer:
            writer.write(snapshot.depth_image.SerializeToString())

    def run(self):
        import os
        import time
        
        # Receive hello message
        print('receiving hello message')
        hello_bytes = self.connection.receive_message()
        print('received hello message')
        hello = Hello.deserialize(hello_bytes)
        
        # Send config message
        print('sending config message')
        #config = Config('timestamp', 'translation', 'rotation',
        #    'color_image', 'depth_image', 'feelings')
        fields = ['pose', 'color_image', 'depth_image', 'feelings']
        config = Config(*fields)
        self.connection.send_message(config.serialize())
        print('config message sent')

        # Receive snapshot message
        snapshot_bytes = self.connection.receive_message()
        snapshot = Snapshot.deserialize(snapshot_bytes)
        self.connection.close()

        self.save_color_image(hello, snapshot)
        self.save_depth_image(hello, snapshot)
        
        snapshot.color_image = cortex_pb2.ColorImage()
        snapshot.depth_image = cortex_pb2.DepthImage()

        #context = object()
        #context.directory = self.data_dir + '/' + str(hello.user_id) + '/' + \
        #    str(snapshot.timestamp)
        #os.mdirs(context.directory, exist_ok=True)
        params = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare('hello')
        channel.basic_publish(exchange='', routing_key='hello',
            body=hello.serialize())
        for field in fields:
            channel.queue_declare(field)
            print(f'sending on {field}: {snapshot.serialize()}')
            data_to_send = hello.user_id.to_bytes(8, 'little') + \
                snapshot.timestamp.to_bytes(8, 'little') + \
                snapshot.serialize()
            channel.basic_publish(exchange='', routing_key=field,
                body=data_to_send)

def server_iteration(listener, publish):
    #TODO take real directory
    client = listener.accept()
    handler = Handler(client, '.', publish)
    handler.start()



@cli.command
def run_server(host, port, publish=print):
    lsnr = Listener(host=host, port=int(port))
    lsnr.start()
    while True:
        p = Process(target=server_iteration,
            args=(lsnr, publish))
        p.start()
        p.join()


if __name__ == '__main__':
    cli.main()
