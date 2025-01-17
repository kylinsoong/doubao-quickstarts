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


API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')


object_key = "test-video-3.mp4"


tos_client = tos.TosClientV2(ak, sk, endpoint, region)

prompt_classification = """你需要分析一组图片，任务是如果有超过2张图片中没人、或为单一背景色，或为黑屏，则回复1，反之回复0。

分析每张图片时，请注意以下几点：
1. 如果图片中没有人物，符合条件。
2. 如果图片是单一背景色（例如全白、全黑、全蓝等），符合条件。
3. 如果图片是黑屏，也符合条件。

逐一检查这些图片，统计符合条件的图片数量。如果这个数量超过2张，回复1，否则回复0。直接给出最终结果，无需任何额外的解释或前言。
"""

prompt_description = """你需要分析一组图片，按顺序将没一张图片所描述的信息累加起来，形成一段话。

分析每张图片时，请注意以下几点：
1. 严格描述图片中的内容，但要求详细描述。
2. 将每一张图片的内容结合起来。
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



def video_object_process(object_key, splittag):
    try:
        tags = tos_client.get_object_tagging(bucket_name, object_key)
        processed_tag_value = None
        for tag in tags.tag_set:
            if tag.key == "processed":
                processed_tag_value = tag.value
                break

        if processed_tag_value is not None:
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
    except tos.exceptions.TosClientError as e:
        return []
    except tos.exceptions.TosServerError as e:
        return []
    except Exception as e:
        return []



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



@log_time
def ark_vision_images(item, prompt, temperature):

    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]

    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=messages,
        temperature=temperature
    )

    return completion


@log_time
def video_classification(frames):
    warpped_frames = process_warpped_frames(frames)
    results = []
    for item in warpped_frames:
        completion = ark_vision_images(item, prompt_classification, 0.01)
        results.append(completion)

    for completion in results:
        print(completion.choices[0].message.content, completion.usage)


@log_time
def video_description(frames):
    warpped_frames = process_warpped_frames(frames)
    results = []
    for item in warpped_frames:
        completion = ark_vision_images(item, prompt_description, 0.7)
        results.append(completion)

    for completion in results:
        print(completion.usage)


@log_time
def main():

    value = str(uuid.uuid4())
    frames = video_object_process(object_key, value)
    video_classification(frames)
    video_description(frames)



if __name__ == '__main__':
    main()
