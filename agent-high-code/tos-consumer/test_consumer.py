import os
import time
from confluent_kafka import Consumer, KafkaError

kafka_endpoint = os.getenv('PUB_SUB_EP')
kafka_topic = os.getenv('PUB_SUB_TOPIC')
group_default = 'group-{}'.format(time.time_ns())

conf = {
    'bootstrap.servers': kafka_endpoint,
    'group.id': group_default,
    'auto.offset.reset': 'earliest'  # optional 'latest'
}


def handle_message(msg):
    print('[INFO] Consumed a message from topic {} [{}] at offset {}. value: {}'.
          format(msg.topic(), msg.partition(), msg.offset(), msg.value().decode('utf-8')))


consumer = Consumer(conf)

consumer.subscribe([kafka_topic])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    elif not msg.error():
        handle_message(msg)
    elif msg.error().code() == KafkaError._PARTITION_EOF:
        print('已经到达分区末尾')
    else:
        print('消费消息时出错: %s' % msg.error())
