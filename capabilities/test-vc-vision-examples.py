import time
import os
import requests
import re
import tos
import uuid
import json
import base64
import numpy as np
import io
from volcenginesdkarkruntime import Ark

base_url = 'https://openspeech.bytedance.com/api/v1/vc'

appid = os.getenv("X_API_APPID")
access_token = os.getenv("X_API_TOKEN")

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')


#####################################################################
# 如下属性需要进行修改
# 视频字幕出现不连续判断阈值
threshold_ms = 8000
# 视频对象的名称
object_key = "sample-video2.mp4"
# 视频对象本地存储路径
object_filename = "/Users/bytedance/Downloads/sample-video2.mp4"

language = 'zh-CN'
#file_url = 'https://tos-cfitc.tos-cn-beijing.volces.com/sample_vedio.mp4'
video_file_prefix = "https://" + bucket_name + "." + endpoint + "/" 

buffer_ac = io.StringIO()
buffer_vision = io.StringIO()


tos_client = tos.TosClientV2(ak, sk, endpoint, region)

prompt = """你需要分析一组图片，任务是如果有超过2张图片中没人、或为单一背景色，或为黑屏，则回复1，反之回复0。

分析每张图片时，请注意以下几点：
1. 如果图片中没有人物，符合条件。
2. 如果图片是单一背景色（例如全白、全黑、全蓝等），符合条件。
3. 如果图片是黑屏，也符合条件。

逐一检查这些图片，统计符合条件的图片数量。如果这个数量超过2张，回复1，否则回复0。直接给出最终结果，无需任何额外的解释或前言。
"""

client = Ark(api_key=API_KEY)

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

@log_time
def upload_tos(object_key, object_filename):
    try:
        result = tos_client.put_object_from_file(bucket_name, object_key, object_filename)
        print('http status code:{}'.format(result.status_code), 'request_id: {}'.format(result.request_id), 'crc64: {}'.format(result.hash_crc64_ecma))
    except tos.exceptions.TosClientError as e:
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
    except tos.exceptions.TosServerError as e:
        print('fail with server error, code: {}'.format(e.code))
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
    except Exception as e:
        print('fail with unknown error: {}'.format(e))


@log_time
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
            print(" 视频预处理...")
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


@log_time
def ac_video_caption(video_file_url):
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
    print('submit response = {}'.format(response.text))
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

@log_time
def analysis_utterances(utterances):
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
        print("字幕检测显示视频不连续(可通过 threshold_ms 设定不连续判断阈值，默认超过8秒不说话则认为视频不连续):")
        for i, interrupt in enumerate(interruptions, 1):
            interruptstr = f"    中断 {i}: 从 {interrupt['gap_start']} 毫秒 到 {interrupt['gap_end']} 毫秒，" + f"出现 {interrupt['gap_duration']} 毫秒的间隔"
            print(interruptstr)
            buffer_ac.write(interruptstr)
            buffer_ac.write("\n")
    else:
        print("视频字幕检查该双录视频是连续的")      


def process_warpped_frames(frames):
    wrapper_list = [frames[i:i + 10] for i in range(0, 100, 10)]
    results = []
    for lst in enumerate(wrapper_list):
        frames = lst[1]
        results.append(frames)
    return results


@log_time
def vedio_to_images():
    base_url = "https://tos-cfitc.tos-cn-beijing.volces.com/sample_video/frame_{:06d}.jpg"
    frame_urls = [base_url.format(i * 60) for i in range(100)]
    wrapper_list = [frame_urls[i:i + 10] for i in range(0, 100, 10)]

    results = []
    for lst in enumerate(wrapper_list):
        frames = lst[1]
        results.append(frames)

    for item in results:
        for img in item:
            print("    ", img)
        time.sleep(2)
    return results

def extract_frame_id(url):
    #match = re.search(r'frame_(\d+)\.jpg', url)
    match = re.search(r'_([\d]+)\.jpg', url)

    if match:
        frame_number = match.group(1)
        return frame_number
    else:
        print("Frame number not found in the URL.")

def print_srage(stage):
    print('-' * 89)
    print(stage)
    print('-' * 89)

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

@log_time
def main():
    print_srage(" 上传视频到对象存储...")
    upload_tos(object_key, object_filename)
    print()
   
    print_srage(" 豆包大模型视频字幕分析阶段...")
    file_url = video_file_prefix + object_key
    print(file_url)
    utterances = ac_video_caption(file_url)
    analysis_utterances(utterances)
    print()

    print_srage(" 视频处理阶段...")
    value = str(uuid.uuid4())
    frames = video_object_process(object_key, value)
    print()

    print_srage(" 豆包大模型视频分析阶段...")
    warpped_frames = process_warpped_frames(frames)
    for item in warpped_frames:
        tag = ark_vision_images(item)
        if "1" in tag:
            interrupts = "     " + extract_frame_id(item[0]) + " 毫秒 - " +  extract_frame_id(item[1]) + " 毫秒出现双录视频未录或黑屏现象"
            print(interrupts)
            buffer_vision.write(interrupts)
            buffer_vision.write("\n")
        else:
            print("    ", extract_frame_id(item[0]), "毫秒 - ", extract_frame_id(item[1]), "毫秒正常")
    print()

    print_srage(" 分析结束")
    if len(buffer_ac.getvalue()) > 0:
        print("视频出现声音不连续或中断")
        print(buffer_ac.getvalue())
        buffer_ac.close()

    if len(buffer_vision.getvalue()) > 0:
        print("视频出现画面不连续或中断")
        print(buffer_vision.getvalue())
        buffer_vision.close()


if __name__ == '__main__':
    main()
