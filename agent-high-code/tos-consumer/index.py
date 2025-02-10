import json
import os
import re
import tos
import base64
import numpy as np
import uuid
from confluent_kafka import Producer

kafka_endpoint = os.getenv('PUB_SUB_EP')
kafka_topic = os.getenv('PUB_SUB_TOPIC')

conf = {
    'bootstrap.servers': kafka_endpoint
}

producer = Producer(conf)

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')
video_file_prefix = "https://" + bucket_name + "." + endpoint + "/"

tos_client = tos.TosClientV2(ak, sk, endpoint, region)

def delivery_report(err, msg):
    if err is not None:
        print(f'视频预处理完成消息发送失败: {err}')
    else:
        print(f'视频预处理完成消息已发送到 {msg.topic()} 分区 {msg.partition()} 偏移量 {msg.offset()}')

def video_object_process(object_key, splittag):
    try:
        tags = tos_client.get_object_tagging(bucket_name, object_key)
        processed_tag_value = None
        for tag in tags.tag_set:
            if tag.key == "processed":
                processed_tag_value = tag.value
                break

        if processed_tag_value is not None:
            print(" 视频预处理完成")
            is_truncated = True
            next_continuation_token = ''
            video_prefix = processed_tag_value + "/"
            video_frames = []
            while is_truncated:
                out = tos_client.list_objects_type2(bucket_name, delimiter="/", prefix=video_prefix, continuation_token=next_continuation_token)
                is_truncated = out.is_truncated
                next_continuation_token = out.next_continuation_token
                for content in out.contents:
                    full_path = "https://" + bucket_name + "." + endpoint + "/" + content.key
                    video_frames.append(full_path)
            frames = []
            frame_prefix = ""
            for frame in video_frames:
                match = re.search(r'_([\d]+)\.jpg', frame)
                if match:
                    extracted_number = match.group(1)
                    frame_prefix = frame[0:len(frame) - len(extracted_number) - 4]
                    frames.append(int(extracted_number))
            sorted_frames = sorted(frames)
            processed_video_frames = []
            for i in sorted_frames:
                processed_video_frames.append(frame_prefix + str(i) + ".jpg")

            return processed_video_frames
        else:
            tag1 = tos.models2.Tag('author', 'cfitc')
            tag2 = tos.models2.Tag('processed', splittag)
            tos_client.put_object_tagging(bucket_name, object_key, [tag1, tag2])
            object_stream = tos_client.get_object(bucket=bucket_name, key=object_key, process="video/info")
            video_info = json.load(object_stream)
            duration = video_info['format']['duration']
            duration = int(float(duration) * 1000)
            values = np.linspace(0, duration, 101, endpoint=False)[1:]
            file_name_with_ext = os.path.basename(object_key)
            file_name = os.path.splitext(file_name_with_ext)[0]
            video_frames = []
            for value in values:
                style = "video/snapshot,t_" + str(int(value))
                save_object = splittag + "/" + file_name + "_" + str(int(value)) + ".jpg"
                save_bucket = bucket_name
                video_frames.append("https://" + save_bucket + "." + endpoint + "/" + save_object)
                tos_client.get_object(
                    bucket=bucket_name,
                    key=object_key,
                    process=style,
                    save_bucket=base64.b64encode(save_bucket.encode("utf-8")).decode("utf-8"),
                    save_object=base64.b64encode(save_object.encode("utf-8")).decode("utf-8")
                )
            return video_frames
    except tos.exceptions.TosClientError as e:
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
        return False
    except tos.exceptions.TosServerError as e:
        print('fail with server error, code: {}'.format(e.code))
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
        return False
    except Exception as e:
        print('fail with unknown error: {}'.format(e))
        return False

def print_srage(stage):
    print('-' * 89)
    print(stage)
    print('-' * 89)

def handler(event, context):
    
    print(f"received new request, event content: {event}", f"context: {context}")

    events = event['data']['events']
    if len(events) > 0 :
        event = events[0]
        object_key = event['tos']['object']['key']
        print("detected object key: ", object_key)
        frames = []
        if object_key.endswith('.mp4'):
            file_url = video_file_prefix + object_key
            print("uploaded file url is: ", file_url)
            print_srage("Video Process...")
            value = str(uuid.uuid4())
            frames = video_object_process(object_key, value)
            msg = {
                'uid': value,
                'video': file_url,
                'split': frames
            }
            msg_bytes = json.dumps(msg).encode('utf-8')
            producer.produce(kafka_topic, msg_bytes, callback=delivery_report)
            producer.flush()
            print(object_key, " process finished.")


    result = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'TOS Process Successed'
        })
    }
    return result


