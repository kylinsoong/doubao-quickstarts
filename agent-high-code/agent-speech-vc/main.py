import os
import time
import json
import io
import requests
from confluent_kafka import Consumer, KafkaError, Producer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Doubao LLM speech vc agent start")

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

consumer = Consumer(conf)
consumer.subscribe([kafka_topic])
logging.info(f"Create consumer: {consumer} subscribe to {kafka_topic}")

producer = Producer(conf_send)
logging.info(f"Create producer: {producer}")

base_url = 'https://openspeech.bytedance.com/api/v1/vc'

appid = os.getenv("X_API_APPID")
access_token = os.getenv("X_API_TOKEN")

default_threshold_ms = 12000
threshold_ms = int(os.getenv("LLM_SPEECH_THRESHOLD_MS", default_threshold_ms))
language = 'zh-CN'



def delivery_report(err, msg):
    if err is not None:
        logging.info(f'消息发送失败: {err}')
    else:
        logging.info(f'消息已发送到 {msg.topic()} 分区 {msg.partition()} 偏移量 {msg.offset()}')



def vc_video_caption(video_file_url):
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

    if response.status_code != 200:
        logging.error(f"Failed to submit video. HTTP status code: {response.status_code}, Response: {response.text}")
        return []

    response_json = response.json()

    if response_json.get('message') != 'Success':
        logging.error(f"Submission unsuccessful. Message: {response_json.get('message')}")
        return []


    job_id = response.json()['id']

    if not job_id:
            logging.error(f"Job ID not found in response. Response: {response.text}")
            return []

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

    if response.status_code != 200:
        logging.error(f"Failed to query job status. HTTP status code: {response.status_code}, Response: {response.text}")
        return []

    utterances = response.json()['utterances']
    return utterances



def analysis_utterances(utterances, buffer_vc):
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
        logging.info("字幕检测显示视频不连续(可通过 threshold_ms 设定不连续判断阈值，默认超过 {threshold_ms} 毫秒不说话则认为视频不连续):")
        for i, interrupt in enumerate(interruptions, 1):
            interruptstr = f"中断 {i}: 从 {interrupt['gap_start']} 毫秒 到 {interrupt['gap_end']} 毫秒，" + f"出现 {interrupt['gap_duration']} 毫秒的间隔"
            logging.info(interruptstr)
            buffer_vc.write(interruptstr)
            buffer_vc.write("\n")
    else:
        logging.info("视频字幕检查该双录视频是连续的")



def handle_message(msg):
    message = json.loads(msg.value().decode('utf-8'))
    uid = message.get('uid', None)
    file_url = message['video']
    if uid is not None and "volces.com" in file_url:
        video_file = file_url.replace("ivolces.com", "volces.com")
        logging.info(f"Doubao speech vc  anslysis {video_file}")
        utterances = vc_video_caption(video_file)
        buffer_vc = io.StringIO()
        analysis_utterances(utterances, buffer_vc)

        logging.info(f"{file_url} anslysis finished")

        msg = {
            'uid': uid,
            'url': file_url,
            'type': "speech",
            'audio': buffer_vc.getvalue(),
            'video': ""
        }
        msg_bytes = json.dumps(msg).encode('utf-8')
        producer.produce(kafka_topic_results, msg_bytes, callback=delivery_report)
        producer.flush()

        logging.info(f"Send Message to {kafka_topic_results}, message: {buffer_vc.getvalue()}")
        buffer_vc.close()



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

