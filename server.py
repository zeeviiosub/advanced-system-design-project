from utils.listener import Listener
import threading
import pathlib
from thought import Thought
from utils.protocol import Hello, Config, Snapshot
from PIL import Image
import cortex_pb2
import json
import pika
from multiprocessing import Process
import cortex_pb2
import matplotlib.pyplot
import numpy
import click

data_dir = '/home/user/advanced-system-design-project/web/static'

@click.group()
def main():
    pass

class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir, publish):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir
        self.publish = publish

    def save_color_image(self, hello, snapshot):
        image = Image.frombytes('RGB', (snapshot.color_image.width, snapshot.color_image.height),
            snapshot.color_image.data)
        image.save(f'{self.data_dir}/{hello.user_id}_{snapshot.timestamp}_color.png', 'png')

    def save_depth_image(self, hello, snapshot):
        A = numpy.array(snapshot.depth_image.data)
        A.shape = (snapshot.depth_image.height, snapshot.depth_image.width)
        matplotlib.pyplot.imsave(f'{self.data_dir}/{hello.user_id}_{snapshot.timestamp}_depth.png', A)

    def run(self):
        import os
        import time
        
        # Receive hello message
        hello_bytes = self.connection.receive_message()
        hello = Hello.deserialize(hello_bytes)
        
        # Send config message
        fields = ['pose', 'color_image', 'depth_image', 'feelings']
        config = Config(*fields)
        self.connection.send_message(config.serialize())

        if type(self.publish) == str:
            params = pika.ConnectionParameters(self.publish)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare('hello')
            channel.basic_publish(exchange='', routing_key='hello',
                body=hello.serialize())
        
        # Receive snapshot message
        snapshot_bytes = self.connection.receive_message()
        snapshot = Snapshot.deserialize(snapshot_bytes)

        print('server: ', snapshot.timestamp)

        self.connection.close()

        self.save_color_image(hello, snapshot)
        self.save_depth_image(hello, snapshot)
        
        snapshot.color_image = cortex_pb2.ColorImage()
        snapshot.depth_image = cortex_pb2.DepthImage()
        
        data_to_send = hello.serialize()
        if type(self.publish) != str:
            self.publish(data_to_send)
        else:
            channel.queue_declare('user')
            channel.basic_publish(exchange='', routing_key='user',
                body=data_to_send)

        for field in fields:
            data_to_send = hello.user_id.to_bytes(8, 'little') + \
                snapshot.timestamp.to_bytes(8, 'little') + \
                snapshot.serialize()
            if type(self.publish) != str:
                self.publish(data_to_send)
            else:
                channel.queue_declare(field)
                channel.basic_publish(exchange='', routing_key=field,
                    body=data_to_send)

def server_iteration(listener, publish):
    client = listener.accept()
    handler = Handler(client, data_dir, publish)
    handler.start()

@main.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=8000)
@click.argument('publish')
def run_server(host, port, publish):
    lsnr = Listener(host=host, port=int(port))
    lsnr.start()
    while True:
        server_iteration(lsnr, publish)


if __name__ == '__main__':
    main()
