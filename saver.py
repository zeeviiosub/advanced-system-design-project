import redis
import click
import pika
import json

@click.group()
def main():
    pass

class Saver:

    def __init__(self, db_url):
        print(db_url)
        self.r = redis.from_url(db_url)

    def save(self, field, data_as_json_string):
        data = json.loads(data_as_json_string)
        user_id = data['user_id']
        timestamp = data['timestamp']
        real_data = data['data']
        print(f'{user_id=}')
        print(f'{timestamp=}')
        print(f'{real_data=}')
        self.r.hset(timestamp, f'{user_id}.{field}', json.dumps(real_data))
        print(f'saved to {user_id}.{field}, {timestamp}')
        print('RESULT:   ', self.r.hget(timestamp, f'{field}.{user_id}'))

@main.command()
@click.option('--database', default='redis://localhost')
@click.argument('topic_name')
@click.argument('data')
def save(database, topic_name, data):
    saver = Saver(db_url)
    saver.save(topic_name, data)
    print(f'{data} saved')

def callback(db_url, field):
    def callback_method(channel, method, properties, body):
        print(db_url)
        saver = Saver(db_url)
        print('NOW SAVING...')
        print(f'saving "{body}" to "{field}"')
        saver.save(field, body)
    return callback_method

@main.command()
@click.option('--database', default='redis://localhost')
@click.argument('queue_name')
def run_saver(database, queue_name):
    print('enter')
    params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue_name)
    #saver = Saver(database)
    print(queue_name)
    channel.basic_consume(queue=queue_name,
                    auto_ack=True,
                    # the name of the field is the name of the queue without
                    # the initial 'save_'
                    on_message_callback=callback(database, queue_name[5:])) 
    channel.start_consuming()

if __name__ == '__main__':
    main()
