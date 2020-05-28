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
            # Send hello message
            print(f'birthday={r.user.birthday}')
            if r.user.gender == 0:
                gender = 'm'
            elif r.user.gender == 1:
                gender = 'f'
            else: # r.user.gender == 2
                gender = 'o'
            hello = protocol.Hello(r.user.user_id,
                r.user.username, r.user.birthday, gender)
            conn.send_message(hello.serialize())
            
            print('receiving config message')
            # Receive config message
            config = protocol.Config.deserialize(conn.receive_message())
            
            # Send snapshot message
            snapshot = protocol.Snapshot(int(time.time()))
            if 'translation' in config.fields:
                snapshot.translation = (
                    s.pose.translation.x,
                    s.pose.translation.y,
                    s.pose.translation.z
                )
            if 'rotation' in config.fields:
                snapshot.rotation = (
                    s.pose.rotation.x,
                    s.pose.rotation.y,
                    s.pose.rotation.z,
                    s.pose.rotation.w
                )
            if 'color_image' in config.fields:
                snapshot.color_image = s.color_image
            if 'depth_image' in config.fields:
                snapshot.depth_image = s.depth_image
            if 'feelings' in config.fields:
                snapshot.hunger, snapshot.thirst, snapshot.exhaustion,
                snapshot.happiness = s.feelings
            print('sending snapshot message')
            conn.send_message(snapshot.serialize())
        return 0
    #except Exception as error:
    #    print(f'ERROR: {error}')
    #    return 1
    finally:
        conn.close()
        print('done')


if __name__ == '__main__':
    cli.main()
