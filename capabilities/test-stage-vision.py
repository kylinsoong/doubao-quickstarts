import time
import re
import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

def extract_frame_id(url):
    match = re.search(r'frame_(\d+)\.jpg', url)

    if match:
        frame_number = match.group(1)
        return frame_number
    else:
        print("Frame number not found in the URL.")

def vedio_to_images():
    base_url = "https://tos-cfitc.tos-cn-beijing.volces.com/sample_video/frame_{:06d}.jpg"
    frame_urls = [base_url.format(i * 60) for i in range(100)]
    wrapper_list = [frame_urls[i:i + 10] for i in range(0, 100, 10)]

    print(" 视频按每 60 帧切片...")
    results = []
    for lst in enumerate(wrapper_list):
        frames = lst[1]
        results.append(frames)

    for item in results:
        for img in item:
            print("    ", img)
        time.sleep(2)
    return results

def ark_vision_images(item):
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "分析图片，如果有超过2 张图片中没人、或为单一背景色，或为黑屏，则回复1，反之回复0"},
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

frames = vedio_to_images()
for item in frames:
    print("    分析帧", extract_frame_id(item[0]), "到", extract_frame_id(item[1]))
    tag = ark_vision_images(item)
    if "1" in tag:
        print("        帧", extract_frame_id(item[0]), "到", extract_frame_id(item[1]),"出现双录视频未现象")
    else:
        print("        正常")


