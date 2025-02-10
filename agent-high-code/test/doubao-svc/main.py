import os
import time
import requests
import json
import io
import re
from confluent_kafka import Consumer, KafkaError, Producer
from volcenginesdkarkruntime import Ark
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Doubao LLM Service Start...")

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
    'max.poll.interval.ms': 600000
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

logging.info("Kafka endpoint: %s, Kafka topic: %s, Kafka results topic: %s, AppID: %s, API Endpoint ID: %s", kafka_endpoint, kafka_topic, kafka_topic_results, appid, API_EP_ID)

client = Ark(api_key=API_KEY)

logging.info("created a ark client")

prompt = """你需要分析一组图片，任务是如果有超过2张图片中没人、或为单一背景色，或为黑屏，则回复1，反之回复0。

分析每张图片时，请注意以下几点：
1. 如果图片中没有人物，符合条件。
2. 如果图片是单一背景色（例如全白、全黑、全蓝等），符合条件。
3. 如果图片是黑屏，也符合条件。

逐一检查这些图片，统计符合条件的图片数量。如果这个数量超过2张，回复1，否则回复0。直接给出最终结果，无需任何额外的解释或前言。
"""

def delivery_report(err, msg):
    if err is not None:
        logging.info(f'消息发送失败: {err}')
    else:
        logging.info(f'消息已发送到 {msg.topic()} 分区 {msg.partition()} 偏移量 {msg.offset()}')


def ark_vision_images(item):
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[0]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[1]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[2]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[3]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[4]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[5]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[6]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[7]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[8]}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url":  item[9]}
                    },
                ],
            }
        ],
        temperature=0.01
    )
    return completion.choices[0].message.content


def ac_video_caption(video_file_url):
    logging.info(f"process: {video_file_url}")
    response = requests.post(
                 '{base_url}/submit'.format(base_url=base_url),
                 params=dict(
                     appid=appid, 
                     language=language,
                     use_itn='True',
                     use_capitalize='True',
                     max_lines=1,
                     words_per_line=15,
                 ),
                 json={
                    'url': video_file_url,
                 },
                 headers={
                    'content-type': 'application/json',
                    'Authorization': 'Bearer; {}'.format(access_token)
                 }
             )
    logging.info('submit response = {}'.format(response.text))
    assert(response.status_code == 200)
    assert(response.json()['message'] == 'Success')

    job_id = response.json()['id']
    response = requests.get(
            '{base_url}/query'.format(base_url=base_url),
            params=dict(
                appid=appid,
                id=job_id,
            ),
            headers={
               'Authorization': 'Bearer; {}'.format(access_token)
            }
    )
    assert(response.status_code == 200)
    utterances = response.json()['utterances']
    return utterances

def analysis_utterances(utterances, buffer_ac):
    interruptions = [] 
    for i in range(len(utterances) - 1):
        current_end = utterances[i]["end_time"]
        next_start = utterances[i + 1]["start_time"]
        
        gap = next_start - current_end
        if gap > threshold_ms:
            interruptions.append({
                "gap_duration": gap,
                "gap_start": current_end,
                "gap_end": next_start
            })
    if len(interruptions):
        logging.info("字幕检测显示视频不连续(可通过 threshold_ms 设定不连续判断阈值，默认超过 12 秒不说话则认为视频不连续):")
        for i, interrupt in enumerate(interruptions, 1):
            interruptstr = f"    中断 {i}: 从 {interrupt['gap_start']} 毫秒 到 {interrupt['gap_end']} 毫秒，" + f"出现 {interrupt['gap_duration']} 毫秒的间隔"
            logging.info(interruptstr)
            buffer_ac.write(interruptstr)
            buffer_ac.write("\n")
    else:
        logging.info("视频字幕检查该双录视频是连续的")
    

def process_warpped_frames(frames):
    wrapper_list = [frames[i:i + 10] for i in range(0, 100, 10)]
    results = []
    for lst in enumerate(wrapper_list):
        frames = lst[1]
        results.append(frames)
    return results

def extract_frame_id(url):
    #match = re.search(r'frame_(\d+)\.jpg', url)
    match = re.search(r'_([\d]+)\.jpg', url)

    if match:
        frame_number = match.group(1)
        return frame_number
    else:
        logging.info("Frame number not found in the URL.")


def handle_message(msg):
    message = json.loads(msg.value().decode('utf-8'))
    uid = message.get('uid', None)  # Default to None if 'uid' is missing
    file_url = message['video']
    if uid is not None and "volces.com" in file_url:
        video_file = file_url.replace("ivolces.com", "volces.com")
        logging.info("豆包大模型视频字幕分析")
        utterances = ac_video_caption(video_file)
        buffer_ac = io.StringIO()
        analysis_utterances(utterances,buffer_ac)

        logging.info("豆包大模型视频分析")
        url_list = message['split']
        new_url_list = list(map(lambda x: x.replace("ivolces.com", "volces.com"), url_list))
        warpped_frames = process_warpped_frames(new_url_list)
        buffer_vision = io.StringIO()
        for item in warpped_frames:
            tag = ark_vision_images(item)
            if "1" in tag:
                interrupts = "     " + extract_frame_id(item[0]) + " 毫秒 - " +  extract_frame_id(item[1]) + " 毫秒出现双录视频未录或黑屏现象"
                logging.info(interrupts)
                buffer_vision.write(interrupts)
                buffer_vision.write("\n")
            else:
                logging.info(f"    {extract_frame_id(item[0])} 毫秒 - {extract_frame_id(item[1])} 毫秒正常")


        logging.info("分析结束")
        msg = {
            'uid': uid,
            'url': file_url,
            'audio': buffer_ac.getvalue(),
            'video': buffer_vision.getvalue()
        }

        msg_bytes = json.dumps(msg).encode('utf-8')
        producer = Producer(conf_send)
        producer.produce(kafka_topic_results, msg_bytes, callback=delivery_report)
        producer.flush()

        logging.info("Send Message to Topic")

        if len(buffer_ac.getvalue()) > 0:
            logging.info("视频出现声音不连续或中断")
            logging.info(buffer_ac.getvalue())
            buffer_ac.close()

        if len(buffer_vision.getvalue()) > 0:
            logging.info("视频出现画面不连续或中断")
            logging.info(buffer_vision.getvalue())
            buffer_vision.close()



consumer = Consumer(conf)

consumer.subscribe([kafka_topic])

logging.info(f"Create consumer: {consumer} subscribe to {kafka_topic}")

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
