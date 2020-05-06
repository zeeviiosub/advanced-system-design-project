import pika
params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='translation')
def callback(channel, method, properties, body):
    print('Debug:   ', body)
channel.basic_consume(
    queue = 'translation',
    auto_ack = True,
    on_message_callback = callback
)
channel.start_consuming()
