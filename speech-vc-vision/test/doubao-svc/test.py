import os
import time
import requests
import json
import io
import re
from confluent_kafka import Consumer, KafkaError, Producer
from volcenginesdkarkruntime import Ark

print("Doubao LLM Service Start...")

kafka_endpoint = os.getenv('PUB_SUB_EP')
kafka_topic = os.getenv('PUB_SUB_TOPIC')
kafka_topic_results = os.getenv('PUB_SUB_TOPIC_RRSULT')
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

conf_send = {
    'bootstrap.servers': kafka_endpoint
}


base_url = 'https://openspeech.bytedance.com/api/v1/vc'

appid = os.getenv("X_API_APPID")
access_token = os.getenv("X_API_TOKEN")

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

threshold_ms = 12000
language = 'zh-CN'

print(kafka_endpoint, kafka_topic, kafka_topic_results, appid, access_token, API_KEY, API_EP_ID)

client = Ark(api_key=API_KEY)

print("created a ark client: ", client)

consumer = Consumer(conf)

consumer.subscribe([kafka_topic])

print("Create consumer: ", consumer, " subscribe to ", kafka_topic)


def handle_message(msg):
    message = json.loads(msg.value().decode('utf-8'))
#    uid = message.get('uid', None)
#    file_url = message['video']
    print(type(message))
    print()
#    if not uid:
#        print("Missing 'uid' in message:", message['video'])
#        return

#    video_file = file_url.replace("ivolces.com", "volces.com")
#    print("豆包大模型视频字幕分析")
    


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
