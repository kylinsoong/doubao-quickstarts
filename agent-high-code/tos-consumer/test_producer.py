import os
import json
from confluent_kafka import Producer

kafka_endpoint = os.getenv('PUB_SUB_EP')
kafka_topic = os.getenv('PUB_SUB_TOPIC')


def delivery_report(err, msg):
    if err is not None:
        print(f'消息发送失败: {err}')
    else:
        print(f'消息已发送到 {msg.topic()} 分区 {msg.partition()} 偏移量 {msg.offset()}')


conf = {
    'bootstrap.servers': kafka_endpoint
}


file_url = "example.mp4"

frames = ['a', 'b', 'c']

msg = {
    'video': file_url,
    'split': frames
}

msg_bytes = json.dumps(msg).encode('utf-8')

producer = Producer(conf)

producer.produce(kafka_topic, msg_bytes, callback=delivery_report)

producer.flush()

print("Send Message to Topic")
