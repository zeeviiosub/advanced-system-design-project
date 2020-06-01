import redis
import click
import pika
import json

@click.group()
def main():
    pass

class Saver:

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
@click.option('--database', default='redis://localhost')
@click.argument('topic_name')
@click.argument('data')
def save(database, topic_name, data):
    saver = Saver(db_url)
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

@main.command()
@click.option('--database', default='redis://localhost')
@click.option('--queue_address', default='localhost')
@click.argument('queue_name')
def run_saver(database, queue_address, queue_name):
    params = pika.ConnectionParameters(queue_address)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue_name)
    channel.basic_consume(queue=queue_name,
                    auto_ack=True,
                    # the name of the field is the name of the queue without
                    # the initial 'save_'
                    on_message_callback=callback(database, queue_name[5:])) 
    channel.start_consuming()

if __name__ == '__main__':
    main()
