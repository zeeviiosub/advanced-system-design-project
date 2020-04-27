import threading
import pathlib
from cli import CommandLineInterface
from listener import Listener
from thought import Thought
from protocol import Hello, Config, Snapshot
from PIL import Image
import cortex_pb2
import json
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

    def run_server(self):
        import os
        hello_bytes = self.connection.receive_message()
        hello = Hello.deserialize(hello_bytes)
        config = Config(['timestamp', 'translation', 'rotation', \
            'color_image', 'depth_image', 'feelings'])
        self.connection.send_message(config.serialize())
        snapshot_bytes = self.connection.receive_message()
        snapshot = Snapshot.deserialize(snapshot_bytes)
        self.connection.close()
        context = object()
        context.directory = self.data_dir / str(hello.user_id) / \
            str(snapshot.datetime)
        os.mdirs(context.directory, exist_ok=True)
        for field in parsers:
            parsers[field](context, snapshot)
#        user_id_bytes = self.connection.receive(8)
#        timestamp_bytes = self.connection.receive(8)
#        thought_sz_bytes = self.connection.receive(4)
#        thought_sz = int.from_bytes(thought_sz_bytes, 'little')
#        thought_bytes = self.connection.receive(thought_sz)
#        self.connection.close()
#        thought = Thought.deserialize(
#            user_id_bytes+timestamp_bytes+thought_sz_bytes+thought_bytes)
#        Handler.lock.acquire()
#        try:
#            user_dir = self.data_dir.joinpath(str(thought.user_id))
#            if not user_dir.exists():
#                user_dir.mkdir()
#            output_file = user_dir.joinpath(
#                thought.timestamp.strftime('%Y-%m-%d_%H-%M-%S') + '.txt')
#            if output_file.exists():
#                open(str(output_file), 'a').write('\n' + thought.thought)
#            else:
#                open(str(output_file), 'w').write(thought.thought)
#        finally:
#            Handler.lock.release()
#

def server_iteration(listener, data):
    client = listener.accept()
    handler = Handler(client, data)
    handler.start()

@cli.command
def run_server(address, data):
    address = (address.split(':')[0], int(address.split(':')[1]))
    data = pathlib.Path(data)
    lsnr = Listener(address[1], host=address[0])
    lsnr.start()
    while True:
        p = Process(target=server_iteration, args=(lsnr, data))
        p.start()
        p.join()


if __name__ == '__main__':
    cli.main()
