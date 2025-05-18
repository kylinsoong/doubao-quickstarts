import json
import os
from volcenginesdkarkruntime import Ark
import logging
import random
import concurrent.futures

logging.basicConfig(level=logging.WARNING,format="%(asctime)s [%(levelname)s] %(message)s",handlers=[logging.StreamHandler()])

models = [os.environ.get("ARK_API_ENGPOINT_ID")] 

def analyze_video(video_url: str, prompt: str):
    if not API_KEY or not API_EP_ID:
        raise ValueError("Missing ARK_API_KEY or ARK_API_ENGPOINT_ID environment variables")

    client = Ark(api_key=API_KEY)

    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "video_url",
                        "video_url": {
                            "url": video_url,
                            "fps": 0.5,
                            "detail": "low"
                        }
                    },
                ],
            }
        ],
        temperature=0.01
    )

    return completion.choices[0].message.content

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)


prompt = """
你是一个视频分类器，负责分析视频截帧的一组图片，并将该视频分类为以下几种类型之一。

### 情景剧
* 画面中包括两人或多人，在室内类似休闲场所，并布置有桌椅、背景装饰，围桌椅而坐，进行日常相互交流讨论。
* 如果画面背景为户外则不属于情景剧

### 采访类
* 面对面采访：画面中采访者拿话筒采访别人
* 户外街访：画面以户外为背景，可能是城市建筑和户外，画面中人站立行进状态，画面中的人接受画面外采访者的采访

注意：上面任何一类采访都属于采访类

### 单人口播
* 所有画面是同一个人，且一直在介绍某个产品，语气专业，有类似对镜头录制的画面
* 如果画面中没有人则不属于单人口播

### 制作类
* 所有图片中没有人，且有多个画面介绍产品

### 解压类
* 图片中包括水彩笔或马克笔等手绘的解压图片，图片类型包括几何解压、流体填充、结构化填色



请根据以上标准对视频进行分类，只输出视频类型，不做额外说明
"""

def load_data():
    expected_path = "expected.json"

    with open(expected_path, 'r') as file:
        expected_results = json.load(file)

    return expected_results

def execute():
    data = load_data()
    for _, entry in enumerate(data):
        expected = entry.get("expected")
        video_url = entry.get("url")
        result = analyze_video(video_url, prompt)

        print(expected, result)


if __name__ == '__main__':
    execute()
