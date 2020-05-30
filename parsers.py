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
import struct
from multiprocessing import Process

cli = CommandLineInterface()

parsers = {}
def parser(field):
    def wrapper(function):
        parsers[field] = function
        return function
    return wrapper

@parser('pose')
def parse_pose(context, snapshot_bytes):
    snapshot = Snapshot.deserialize(snapshot_bytes)
    return {'translation': snapshot.translation,
            'rotation': snapshot.rotation}
    #return struct.pack('fffffff',
    #    snapshot.translation[0],
    #    snapshot.translation[1],
    #    snapshot.translation[2],
    #    snapshot.rotation[0],
    #    snapshot.rotation[1],
    #    snapshot.rotation[2],
    #    snapshot.rotation[3])
#@parser('translation')
#def parse_translation(context, snapshot_bytes):
#    print('parse translation')
#    snapshot = Snapshot.deserialize(snapshot_bytes)
#    with open(context.directory / 'translation.json') as writer:
#        json.dump(snapshot.translation, writer)
#    with open(context.directory / 'translation.json') as reader:
#        return reader.read()
#parse_translation.field = 'translation'

@parser('color_image')
def parse_color_image(context, snapshot_bytes):
    snapshot = Snapshot.deserialize(snapshot_bytes)
    return f'{context.user_id}_{snapshot.timestamp}_color_image.json'

@parser('depth_image')
def parse_depth_image(context, snapshot_bytes):
    snapshot = Snapshot.deserialize(snapshot_bytes)
    return f'{context.user_id}_{snapshot.timestamp}_depth_image.json'

@parser('feelings')
def parse_feelings(context, snapshot_bytes):
    snapshot = Snapshot.deserialize(snapshot_bytes)
    return {'hunger': snapshot.hunger,
            'thirst': snapshot.thirst,
            'exhaustion': snapshot.exhaustion,
            'happiness': snapshot.happiness}
    #struct.pack('ffff',
     #   snapshot.hunger,
    #    snapshot.thirst,
    #    snapshot.exhaustion,
    #    snapshot.happiness)

#@parser('color_image')
#def parse_color_image(context, snapshot):
#    print('parsing colour image')
#    snapshot = 

#    with open(context.directory / 'color_image.jpg', 'w') as writer:
#        json.dump(snapshot.color_image, writer)
#parse_color_image.field = 'color_image'

def parse_field(context, body):
    with open(context.directory / 'tmp.json', 'w') as writer:
        json.dump(body, writer)
    with open(context.directory / 'tmp.json') as reader:
        return reader.read()


#@parser('pose')
#def parse_pose(context, pose):
#    return Snapshot.deserialize_pose(pose_bytes)

#@parser('depth_image')
#def parse_depth_image(context, depth_image_bytes):
#    return Snapshot.deserialize_depth_image(depth_image_bytes)
#    with open(context.directory / 'depth_image.json', 'w') as writer:
#        json.dump(snapshot.depth_image, writer)
#parse_depth_image.field = 'depth_image'

#@parser('rotation')
#def parse_rotation(context, snapshot_bytes):
#    print('parsing rotation')
#    snapshot = Snapshot.deserialize(snapshot_bytes)
#    with open(context.directory / 'rotation.json', 'w') as writer:
#        json.dump(snapshot.rotation, writer)
#    with open(context.directory / 'rotation.json', 'r') as reader:
#        return reader.read()
#parse_rotation.field = 'rotation'

#@parser('feelings')
#def parse_feelings(context, feelings_bytes):
#    return Snapshot.deserialize_feelings(feelings_bytes)
#    context.save('feelings.json', json.dumps(dict(
#        hunger = snapshot.feelings.hunger,
#        thirst = snapshot.feelings.thirst,
#        happiness = snapshot.feelings.happiness,
#        exhaustion = snapshot.feelings.exhaustion
#    )))
#parse_feelings.field = 'feelings'

class Context:
    def __init__(self, user_id):
        import pathlib
        self.directory = pathlib.Path('/home/user/advanced-system-design-project')
        self.user_id = user_id

#def get_context(): #TODO
#    import pathlib
#    context = Context()
#    context.directory = pathlib.Path('/home/user/advanced-system-design-project')
#    return context

#def parse(field, data):
#    return field + '*' + parse_field(Context(), deserializers[field](data))

def callback(field):
    def callback_method(channel, method, properties, body):
        #print('PARSERS:  received message')
        context = Context(int.from_bytes(body[0:8], 'little'))
        result = parsers[field](context, body[16:])
        params = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(params)
        new_channel = connection.channel()
        new_channel.queue_declare(f'save {field}')
        #print(f'PARSERS:  sending on save {field}')
        json_to_send = json.dumps({'user_id': context.user_id,
                                   'timestamp': int.from_bytes(body[8:16], 'little'),
                                   'data': result})
        new_channel.basic_publish(
            exchange='',
            routing_key=f'save_{field}',
            body=json_to_send)
        #print(f'PARSERS:  published "{json_to_send}" to save_{field}')
    return callback_method

@cli.command
def run_parser(field, queue_address):
    params = pika.ConnectionParameters(queue_address)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=field)
    #print('PARSERS:  consuming on parsers')
    channel.basic_consume(
        queue=field,
        auto_ack=True,
        on_message_callback=callback(field)
    )
    channel.start_consuming()


if __name__ == '__main__':
    cli.main()

#params = pika.ConnectionParameters('localhost')
#connection = pika.BlockingConnection(params)
#channel = connection.channel()
#channel.queue_declare(queue='translation')
#def callback(channel, method, properties, body):
#    snapshot = Snapshot.deserialize(body)
#    context.save('translation.json', json.dumps(dict(
#        x = snapshot.pose.translation.x,
#        y = snapshot.pose.translation.y,
#        z = snapshot.pose.translation.z,
#    )))
#channel.basic_consume(
#    queue = 'translation',
#    auto_ack = True,
#    on_message_callback = callback
#)
#channel.start_consuming()
