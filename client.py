from utils.connection import Connection
from thought import Thought
from datetime import datetime
import utils.protocol
import click

@click.group()
def main():
    pass

@main.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=8000)
@click.argument('file_name')
def upload_sample(host, port, file_name):
    import socket
    import time
    import reader
    try:
        address = (host, port)
        r = reader.Reader(file_name)
        i = 0
        for s in r:
            soc = socket.socket()
            soc.connect(address)
            conn = Connection(soc)
            
            try:
                # Send hello message
                if r.user.gender == 0:
                    gender = 'm'
                elif r.user.gender == 1:
                    gender = 'f'
                else: # r.user.gender == 2
                    gender = 'o'
                hello = utils.protocol.Hello(r.user.user_id,
                    r.user.username, r.user.birthday, gender)
                conn.send_message(hello.serialize())

                # Receive config message
                config = utils.protocol.Config.deserialize(conn.receive_message())

                # Send snapshot message
                snapshot = utils.protocol.Snapshot(s.datetime)
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
                    snapshot.hunger = s.feelings.hunger
                    snapshot.thirst = s.feelings.thirst
                    snapshot.exhaustion = s.feelings.exhaustion
                    snapshot.happiness = s.feelings.happiness
                conn.send_message(snapshot.serialize())
                i = i + 1
                print(i)
            except Exception as e:
                raise e
            finally:
                conn.close()
        return 0
    except Exception as error:
        raise error
        print(f'ERROR: {error}')
        return 1
    finally:
        print('done')


if __name__ == '__main__':
    main()
