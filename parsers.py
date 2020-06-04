import click
import threading
import pathlib
from utils.protocol import Hello, Config, Snapshot
from PIL import Image
import utils.cortex_pb2
import json
import pika
import struct
from multiprocessing import Process
from urllib.parse import urlparse

image_data_dir = '../../static'

@click.group()
def main():
    pass

parsers = {}
def parser(field):
    def wrapper(function):
        parsers[field] = function
        return function
    return wrapper

@parser('pose')
def parse_pose(context, snapshot_bytes):
    snapshot = Snapshot.deserialize(snapshot_bytes[16:])
    return {'translation': snapshot.translation,
            'rotation': snapshot.rotation}

@parser('color_image')
def parse_color_image(context, snapshot_bytes):
    snapshot = Snapshot.deserialize(snapshot_bytes[16:])
    return f'{image_data_dir}/{context.user_id}_{snapshot.timestamp}_color.png'

@parser('depth_image')
def parse_depth_image(context, snapshot_bytes):
    snapshot = Snapshot.deserialize(snapshot_bytes[16:])
    return f'{image_data_dir}/{context.user_id}_{snapshot.timestamp}_depth.png'

@parser('feelings')
def parse_feelings(context, snapshot_bytes):
    snapshot = Snapshot.deserialize(snapshot_bytes[16:])
    return {'hunger': snapshot.hunger,
            'thirst': snapshot.thirst,
            'exhaustion': snapshot.exhaustion,
            'happiness': snapshot.happiness}

@parser('user')
def parse_user(context, user_bytes):
    user = Hello.deserialize(user_bytes)
    return {'user_id': user.user_id,
            'username': user.username,
            'birth_date': user.birth_date,
            'gender': user.gender}

class Context:
    def __init__(self, user_id):
        import pathlib
        self.directory = pathlib.Path('/home/user/advanced-system-design-project')
        self.user_id = user_id


def callback(field, queue_address):
    def callback_method(channel, method, properties, body):
        try:
            context = Context(int.from_bytes(body[0:8], 'little'))
            result = parsers[field](context, body)
            params = pika.ConnectionParameters(queue_address)
            connection = pika.BlockingConnection(params)
            new_channel = connection.channel()
            new_channel.queue_declare(f'save_{field}')
            if field == 'user':
                json_to_send = json.dumps(result)
            else:
                json_to_send = json.dumps({'user_id': context.user_id,
                                           'timestamp': int.from_bytes(body[8:16], 'little'),
                                           'data': result})
            new_channel.basic_publish(
                exchange='',
                routing_key=f'save_{field}',
                body=json_to_send)
        except Exception:
            pass
    return callback_method

def parse(field, data):
    parsers[field](data)

@main.command()
@click.argument('field')
@click.argument('path')
def parse(field, path):
    with open(path, 'rb') as f:
        data = f.read()
    parsers[field](data)

@main.command()
@click.argument('field')
@click.argument('queue_address')
def run_parser(field, queue_address):
    
    params = pika.ConnectionParameters(queue_address)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=field)
    channel.basic_consume(
        queue=field,
        auto_ack=True,
        on_message_callback=callback(field, queue_address)
    )
    channel.start_consuming()


if __name__ == '__main__':
    main()
