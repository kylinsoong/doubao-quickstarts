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

default_prompt = """你需要分析一组图片，任务是如果有超过2张图片中没人、或为单一背景色，或为黑屏，则回复1，反之回复0。

分析每张图片时，请注意以下几点：
1. 如果图片中没有人物，符合条件。
2. 如果图片是单一背景色（例如全白、全黑、全蓝等），符合条件。
3. 如果图片是黑屏，也符合条件。

逐一检查这些图片，统计符合条件的图片数量。如果这个数量超过2张，回复1，否则回复0。直接给出最终结果，无需任何额外的解释或前言。
"""
default_batch_size = 10

prompt = os.getenv("LLM_VISION_USER_PROMPT", default_prompt)
vision_batch_size = int(os.getenv("LLM_VISION_BATCH_SIZE", default_batch_size))

client = Ark(api_key=API_KEY)
logging.info(f"Create a Ark client: {client}, vison batch sieze: {default_batch_size}, prompt: {prompt}")

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


def process_batched_frames(frames):
    wrapper_list = [frames[i:i + 10] for i in range(0, 100, 10)]
    results = []
    for lst in enumerate(wrapper_list):
        frames = lst[1]
        results.append(frames)
    return results


def ark_vision_images(item):

    numbers = [re.search(r'_(\d+)\.jpg', url).group(1) for url in item if re.search(r'_(\d+)\.jpg', url)]
    if not numbers:
        logging.warning("No valid image URLs found in the input.")
        return None, None, None
    time_start = numbers[0]
    time_end = numbers[-1]
    logging.info(f"process {time_start} to {time_end}")

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

        return completion.choices[0].message.content, time_start, time_end

    except Exception as e:
        logging.error(f"Error while calling the API: {str(e)}")
        return None, time_start, time_end





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
        #batched_frames = split_frames_into_batches(url_list, batch_size=vision_batch_size)
        new_url_list = list(map(lambda x: x.replace("ivolces.com", "volces.com"), url_list))
        batched_frames = split_frames_into_batches(new_url_list, batch_size=vision_batch_size)
        buffer_vision = io.StringIO()
        for item in batched_frames:
            tag, time_start, time_end = ark_vision_images(item)
            if tag is None and time_start is None and time_end is None:
                logging.warning(f"Invalid items: {item}")
            elif tag is None:
                logging.warning(f"{time_start} 毫秒 - {time_end} 毫秒: 无法判断分析结果")
            elif "1" in tag:
                interrupts = f"{time_start} 毫秒 - {time_end} 毫秒出现双录视频未录或黑屏现象"
                logging.info(interrupts)
                buffer_vision.write(interrupts)
                buffer_vision.write("\n")
            else:
                logging.info(f"{time_start} 毫秒 - {time_end} 毫秒正常")

        logging.info(f"{file_url} anslysis finished")

        msg = {
            'uid': uid,
            'url': file_url,
            'type': "vision",
            'audio': "",
            'video': buffer_vision.getvalue()
        }
        msg_bytes = json.dumps(msg).encode('utf-8')
        producer.produce(kafka_topic_results, msg_bytes, callback=delivery_report)
        producer.flush()

        logging.info(f"Send Message to {kafka_topic_results}, message: {buffer_vision.getvalue()}")
        buffer_vision.close()




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
