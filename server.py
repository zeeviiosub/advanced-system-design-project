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

cli = CommandLineInterface()

parsers = {}
def parser(field):
    def wrapper(function):
        parsers[field] = function
        return function
    return wrapper

@parser('translation')
def parse_translation(context, snapshot):
    context.save('translation.json', json.dumps(dict(
        x = snapshot.pose.translation.x,
        y = snapshot.pose.translation.y,
        z = snapshot.pose.translation.z,
    )))
parse_translation.field = 'translation'

@parser('color_image')
def parse_color_image(context, snapshot):
    with open(context.directory / 'color_image.jpg', 'w') as writer:
        json.dump(snapshot.color_image, writer)
parse_color_image.field = 'color_image'

@parser('depth_image')
def parse_depth_image(context, snapshot):
    with open(context.directory / 'depth_image.json', 'w') as writer:
        json.dump(snapshot.depth_image, writer)
parse_depth_image.field = 'depth_image'

@parser('rotation')
def parse_rotation(context, snapshot):
    with open(context.directory / 'rotation.json', 'w') as writer:
        json.dump(snapshot.rotation, writer)
parse_rotation.field = 'rotation'

@parser('feelings')
def parse_feelings(context, snapshot):
    context.save('feelings.json', json.dumps(dict(
        hunger = snapshot.feelings.hunger,
        thirst = snapshot.feelings.thirst,
        happiness = snapshot.feelings.happiness,
        exhaustion = snapshot.feelings.exhaustion
    )))
parse_feelings.field = 'feelings'

class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        import os
        import time
        hello_bytes = self.connection.receive_message()
        hello = Hello.deserialize(hello_bytes)
        config = Config('timestamp', 'translation', 'rotation',
            'color_image', 'depth_image', 'feelings')
        time.sleep(6)
        self.connection.send_message(config.serialize())
        snapshot_bytes = self.connection.receive_message()
        snapshot = Snapshot.deserialize(snapshot_bytes)
        self.connection.close()
        context = object()
        context.directory = self.data_dir / str(hello.user_id) / \
            str(snapshot.datetime)
        os.mdirs(context.directory, exist_ok=True)
        params = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        for field in parsers:
            channel.queue_declare(field)
            channel.basic_publish(exchange='', routing_key=field,
                body=snapshot)
        #for field in parsers:
        #    parsers[field](context, snapshot)

def server_iteration(listener, publish):
    client = listener.accept()
    handler = Handler(client, publish)
    handler.start()


#def run_server(host, port, publish):
#    lsnr = Listener(port, host=host)
#    lsnr.start()
#    while True:
#        p = Process(target=server_iteration, args=(lsnr, publish))
#        p.start()
#        p.join()

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
