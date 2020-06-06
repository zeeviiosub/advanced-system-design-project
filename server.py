from utils.listener import Listener
import threading
import pathlib
from utils.protocol import Hello, Config, Snapshot
from PIL import Image
import utils.cortex_pb2
import json
import pika
from multiprocessing import Process
import matplotlib.pyplot
import numpy
import click
import os

data_dir = os.path.split(os.path.abspath(__file__))[0] + '/web/static'

fields = ['pose', 'color_image', 'depth_image', 'feelings']


@click.group()
def main():
    pass

def publish_on_queue(queue):
    def publish_function(hello, snapshot):
        params = pika.ConnectionParameters(queue)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        data_to_send = hello.serialize()
        channel.queue_declare('user')
        channel.basic_publish(exchange='', routing_key='user',
            body=data_to_send)
        
        for field in fields:
            data_to_send = hello.user_id.to_bytes(8, 'little') + \
                snapshot.timestamp.to_bytes(8, 'little') + \
                snapshot.serialize()
            channel.queue_declare(field)
            channel.basic_publish(exchange='', routing_key=field,
                body=data_to_send)
    return publish_function

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
        config = Config(*fields)
        self.connection.send_message(config.serialize())

        # Receive snapshot message
        snapshot_bytes = self.connection.receive_message()
        snapshot = Snapshot.deserialize(snapshot_bytes)

        print('server: ', snapshot.timestamp)

        self.connection.close()

        self.save_color_image(hello, snapshot)
        self.save_depth_image(hello, snapshot)
        
        snapshot.color_image = utils.cortex_pb2.ColorImage()
        snapshot.depth_image = utils.cortex_pb2.DepthImage()
        
        self.publish(hello, snapshot)

def server_iteration(listener, publish):
    client = listener.accept()
    handler = Handler(client, data_dir, publish)
    handler.start()

def run_cortex_server(host, port, publish):
    lsnr = Listener(host=host, port=int(port))
    lsnr.start()
    while True:
        server_iteration(lsnr, publish)
    

@main.command()
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=8000)
@click.argument('queue')
def run_server(host, port, queue):
    run_cortex_server(host, port, publish_on_queue(queue))


if __name__ == '__main__':
    main()
