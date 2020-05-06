from cli import CommandLineInterface
from utils.connection import Connection
from thought import Thought
from datetime import datetime
import protocol


cli = CommandLineInterface()


@cli.command
def upload_thought(address, file_name):
    import socket
    import time
    import reader
    try:
        address = (address.split(':')[0], int(address.split(':')[1]))
        s = socket.socket()
        s.connect(address)
        conn = Connection(s)
        r = reader.Reader(file_name)
        for s in r:
            hello = protocol.Hello(r.user.user_id,
                r.user.username, r.user.birthday, r.user.gender)
            conn.send(hello.serialize())
            config = protocol.Config.deserialize(conn.receive_message())
            snapshot = protocol.Snapshot()
            if 'translation' in config.fields:
                snapshot.translation = s.pose.translation
            if 'rotation' in config.fields:
                snapshot.rotation = s.pose.rotation
            if 'color_image' in config.fields:
                snapshot.color_image = s.color_image
            if 'depth_image' in config.fields:
                snapshot.depth_image = s.depth_image
            if 'feelings' in config.fields:
                snapshot.hunger, snapshot.thirst, snapshot.exhuastion, \
                snapshot.happiness = s.feelings
            conn.send(snapshot.serialize())
        config_bytes = conn.receive_message()
        thought_obj = \
            Thought(user, datetime.fromtimestamp(int(time.time())), thought)
        conn.send(thought_obj.serialize())
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1
    finally:
        conn.close()
        print('done')


if __name__ == '__main__':
    cli.main()
