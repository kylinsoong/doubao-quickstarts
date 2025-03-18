import json
import os
from volcenginesdkarkruntime import Ark

def ark_vision_images(item, prompt, temperature):
    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]
    try:
        completion = client.chat.completions.create(
            model=API_EP_ID,
            messages=messages,
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return None

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

source = "/Users/bytedance/Downloads/tmp/360/data.json"

with open(source, 'r') as file:
    data = json.load(file)

keys = list(data.keys())

prompt = """
# 角色
你是一个视频分类器，分析视频截帧的一组图片并对视频进行分类标记。

# 任务
分析视频截帧的一组图片，并将其分类为一下几种类型之一

## 情景剧
* 画面中包括两人或三人交流，通过肢体语言和表情传递情节信息，场景为室内类似休闲场所，布置有桌椅、背景装饰等，营造日常交流氛围。
* 如果画面背景为户外则不属于情景剧

## 采访类
* 面对面采访：画面中采访者拿话筒采访别人
* 户外街访：画面以户外为背景，可能是城市建筑和户外，画面中多数图片是画面中的人接受画面外采访者的采访

注意：上面任何一类采访都属于采访类

## 单人口播
* 所有图片中是同一个人，且一直在介绍某个产品，语气专业，有类似对镜头录制的画面

## 制作类
* 所有图片中没有人，且有多个画面介绍产品

## 解压类
* 图片中包括水彩笔等手绘的解压图片

# 要求

根据#任务部分分类根系图片，只输出类型，不做额外输出
"""

expected_path = "expected.json"
with open(expected_path, 'r') as file:
    expected_results = json.load(file)

for key in keys:
    result = ark_vision_images(data[key], prompt, 0.1)
    print(key, result, expected_results[key])

