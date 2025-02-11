import os
import time
import json
import io
import re
from confluent_kafka import Consumer, KafkaError, Producer
from volcenginesdkarkruntime import Ark
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Doubao LLM vison agent start")

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

default_batch_size = 10
vision_batch_size = int(os.getenv("LLM_VISION_BATCH_SIZE", default_batch_size))

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
    'auto.commit.interval.ms': 1000,
    'max.poll.interval.ms': 300000
}

conf_send = {
    'bootstrap.servers': kafka_endpoint
}

default_prompt = """
你将执行一个分析一组图片的任务，任务的结果是判断图片中是否有给机车加油动作，结果有两种：正常加油和没有加油。并且需要按照特定的判断逻辑得出结论，最后以JSON格式输出结果，格式为{"result":"正常加油/没有加油", "reason":"判断的原因"}。

下面是判断逻辑：
1. 如果图片中包括给汽车加油的动作，才有可能是正常加油情况。这里的汽车加油动作指油枪连接着汽车的油箱并且加油过程持续一定时间。
2. 正常加油的情况下，加油时间较长，通常需要3张以上的图片显示油枪连接着汽车的邮箱。
3. 在得出结论后，需要简单总结得出该结论的原因。

请按照上述判断逻辑分析图片，然后在<answer>标签内以JSON格式输出结果，格式为{"result":"正常加油/没有加油", "reason":"判断的原因"}。
"""

prompt = os.getenv("LLM_VISION_USER_PROMPT", default_prompt)

client = Ark(api_key=API_KEY)
logging.info(f"Create a Ark client: {client}, prompt: {prompt}")

consumer = Consumer(conf)
consumer.subscribe([kafka_topic])
logging.info(f"Create consumer: {consumer} subscribe to {kafka_topic}")

producer = Producer(conf_send)
logging.info(f"Create producer: {producer}")


def split_frames_into_batches(frames, batch_size=10):
    if not frames or not isinstance(frames, list):
        logging.warning("Invalid or empty frames input.")
        return []
    return [frames[i:i + batch_size] for i in range(0, len(frames), batch_size)]


def ark_vision_images(item):

    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]

    try:
        completion = client.chat.completions.create(
            model=API_EP_ID,
            messages=messages,
            temperature=0.01
        )

        return completion.choices[0].message.content

    except Exception as e:
        logging.error(f"Error while calling the API: {str(e)}")
        return None





def delivery_report(err, msg):
    if err is not None:
        logging.info(f'消息发送失败: {err}')
    else:
        logging.info(f'消息已发送到 {msg.topic()} 分区 {msg.partition()} 偏移量 {msg.offset()}')



def handle_message(msg):
    message = json.loads(msg.value().decode('utf-8'))
    uid = message.get('uid', None) 
    file_url = message['video']
    if uid is not None and "volces.com" in file_url:
        logging.info(f"Doubao Vision anslysis {file_url}")
        url_list = message['split']
        new_url_list = list(map(lambda x: x.replace("ivolces.com", "volces.com"), url_list))
        batched_frames = split_frames_into_batches(new_url_list, batch_size=vision_batch_size)
        results = None
        for item in batched_frames:
            results = ark_vision_images(item)
            if results and isinstance(results, str):
                results_json = json.loads(results)
                if results_json.get("result") == "正常加油":
                    break

        if results is not None:
            logging.info(f"{file_url} anslysis finished, results: {results}")

            msg = {
                'uid': uid,
                'url': file_url,
                'type': "vision",
                'video': results
            }
            msg_bytes = json.dumps(msg).encode('utf-8')
            producer.produce(kafka_topic_results, msg_bytes, callback=delivery_report)
            producer.flush()

            logging.info(f"Send Message to {kafka_topic_results}, message: {msg}")
        else:
            logging.error(f"Analysis failed for {file_url}, no results returned.")


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
