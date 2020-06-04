import redis
import click
import pika
import json
import threading
from urllib.parse import urlparse

@click.group()
def main():
    pass

class Saver():

    def __init__(self, db_url):
        self.r = redis.from_url(db_url)

    def save_field(self, field, data_as_json_string):
        data = json.loads(data_as_json_string)
        user_id = data['user_id']
        timestamp = data['timestamp']
        real_data = data['data']
        
        fields_array = self.r.hget(f'{user_id}.fields', timestamp)
        if fields_array:
            fields_array = json.loads(fields_array.decode('utf8'))
            if field not in fields_array:
                fields_array.append(field)
        else:
            fields_array = [field]

        snapshots_array = self.r.hget('snapshots', user_id)
        if snapshots_array:
            snapshots_array = json.loads(snapshots_array.decode('utf8'))
            if timestamp not in snapshots_array:
                snapshots_array.append(timestamp)
        else:
            snapshots_array = [timestamp]
        self.r.hset('snapshots', user_id, json.dumps(snapshots_array))
        self.r.hset(f'{user_id}.fields', timestamp, json.dumps(fields_array))
        self.r.hset(f'{user_id}.{field}', timestamp, json.dumps(real_data))

    def save_user(self, data_as_json_string):
        data = json.loads(data_as_json_string)
        user_id = data['user_id']
        self.r.hset('user', user_id, data_as_json_string)
        

@main.command()
@click.option('--database', '-d', default='redis://localhost')
@click.argument('topic_name')
@click.argument('path')
def save(database, topic_name, path):
    saver = Saver(db_url)
    with open('path', 'rb') as f:
        data = f.read
    saver.save_field(topic_name, data)

def callback(db_url, field):
    def callback_method(channel, method, properties, body):
        try:
            saver = Saver(db_url)
            if method.routing_key == 'save_user':
                saver.save_user(body)
            else:
                print(f'saving {field}')
                saver.save_field(field, body)
        except Exception:
            pass
    return callback_method

class SaverThread(threading.Thread):
    def __init__(self, queue_hostname, database, queue_name):
        super().__init__()
        self.queue_name = queue_name
        self.queue_hostname = queue_hostname
        self.database = database
    def run(self):
        print(f'thread: {self.queue_name}, {self.database}')
        params = pika.ConnectionParameters(self.queue_hostname)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(self.queue_name)
        channel.basic_consume(queue=self.queue_name,
                        auto_ack=True,
                        # the name of the field is the name of the queue without
                        # the initial 'save_'
                        on_message_callback=callback(self.database, self.queue_name[5:])) 
        channel.start_consuming()
        

@main.command()
@click.argument('database')
@click.argument('queue')
def run_saver(database, queue):
    queue_url = urlparse(queue)
    if queue_url.scheme != 'rabbitmq':
        click.echo('Wrong message queue. Only rabbitmq is supported.')
    if queue_url.port != 5672:
        click.echo('Wrong port. The port for rabbitmq is 5672.')
    threads = {}
    queue_names = ['save_user', 'save_pose', 'save_feelings', 'save_color_image', 'save_depth_image']
    for queue_name in queue_names:
        threads[queue_name] = SaverThread(queue_url.hostname, database, queue_name)
        threads[queue_name].start()
    for queue_name in queue_names:
        threads[queue_name].join()

if __name__ == '__main__':
    main()
