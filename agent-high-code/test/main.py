import os
import time
import json
import logging
from confluent_kafka import Consumer, KafkaError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

kafka_endpoint = os.getenv('PUB_SUB_EP')
kafka_topic = os.getenv('PUB_SUB_TOPIC_TEST')
group_default = 'group-{}'.format(time.time_ns())
reset_default = 'earliest' 
commit_default = 'True'

conf = {
    'bootstrap.servers': kafka_endpoint,  
    'group.id': group_default,
    'auto.offset.reset': reset_default, 
    'enable.auto.commit': commit_default,
    'auto.commit.interval.ms': 1000
}


def handle_message(msg):
    message = json.loads(msg.value().decode('utf-8'))
    logging.info(message)


consumer = Consumer(conf)

consumer.subscribe([kafka_topic])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    elif not msg.error():
        handle_message(msg)
    elif msg.error().code() == KafkaError._PARTITION_EOF:
        logging.info('已经到达分区末尾')
    else:
        logging.info('消费消息时出错: %s' % msg.error())
