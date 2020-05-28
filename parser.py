import pika
from protocol import Snapshot
params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='translation')
def callback(channel, method, properties, body):
    snapshot = Snapshot.deserialize(body)
    context.save('translation.json', json.dumps(dict(
        x = snapshot.pose.translation.x,
        y = snapshot.pose.translation.y,
        z = snapshot.pose.translation.z,
    )))
channel.basic_consume(
    queue = 'translation',
    auto_ack = True,
    on_message_callback = callback
)
channel.start_consuming()
#@parser('translation')
#def parse_translation(context, snapshot):
#    context.save('translation.json', json.dumps(dict(
#        x = snapshot.pose.translation.x,
#        y = snapshot.pose.translation.y,
#        z = snapshot.pose.translation.z,
#    )))
#parse_tVranslation.field = 'translation'
