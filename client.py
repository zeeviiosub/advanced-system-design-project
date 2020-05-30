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
            print(s.datetime)
            print(s.feelings)
            if r.user.gender == 0:
                gender = 'm'
            elif r.user.gender == 1:
                gender = 'f'
            else: # r.user.gender == 2
                gender = 'o'
            hello = protocol.Hello(r.user.user_id,
                r.user.username, r.user.birthday, gender)
            print('sending hello message')
            conn.send_message(hello.serialize())
            
            print('receiving config message')
            # Receive config message
            config = protocol.Config.deserialize(conn.receive_message())
            
            # Send snapshot message
            snapshot = protocol.Snapshot(s.datetime)
            if 'pose' in config.fields and s.pose:
                snapshot.translation = (
                    s.pose.translation.x,
                    s.pose.translation.y,
                    s.pose.translation.z
                )
                snapshot.rotation = (
                    s.pose.rotation.x,
                    s.pose.rotation.y,
                    s.pose.rotation.z,
                    s.pose.rotation.w
                )
            if 'color_image' in config.fields and s.color_image:
                snapshot.color_image = s.color_image
            if 'depth_image' in config.fields and s.depth_image:
                snapshot.depth_image = s.depth_image
            if 'feelings' in config.fields and s.feelings:
                print(s.feelings)
                snapshot.hunger = s.feelings.hunger
                snapshot.thirst = s.feelings.thirst
                snapshot.exhaustion = s.feelings.exhaustion
                snapshot.happiness = s.feelings.happiness
            print('sending snapshot message')
            conn.send_message(snapshot.serialize())
        return 0
    except Exception as error:
        raise error
        print(f'ERROR: {error}')
        return 1
    finally:
        conn.close()
        print('done')


if __name__ == '__main__':
    cli.main()
