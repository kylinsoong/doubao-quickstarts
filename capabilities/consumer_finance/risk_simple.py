#!/usr/bin/env python3

import os
import argparse
from volcenginesdkarkruntime import Ark

def ark_vision_images(client, API_EP_ID, item, prompt, temperature):
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
        return completion.choices[0].message.content, completion.usage
    except Exception as e:
        return str(e)

def main():
    parser = argparse.ArgumentParser(description='Process ARK API parameters and images.')
    parser.add_argument('--ARK_API_KEY', type=str, required=True, help='ARK API Key')
    parser.add_argument('--ARK_API_ENGPOINT_ID', type=str, required=True, help='ARK API Endpoint ID')
    parser.add_argument('--images', nargs='+', required=True, help='List of image URLs')

    args = parser.parse_args()

    API_KEY = args.ARK_API_KEY
    API_EP_ID = args.ARK_API_ENGPOINT_ID
    images = args.images

    client = Ark(api_key=API_KEY)

    prompt = """
你的任务是分析一组图片，分析结果将用于贷款授信。你需要仔细观察图片，分析图片中人的性别、年龄、表情、背景、是否戴眼镜。

请从以下几个维度进行分析：
1. 性别：明确图片中人的性别，只能填写"男"或"女"。
2. 年龄：判断图片中人的年龄，以年龄段的形式表示，例如"30 - 35""35 - 40"等。
3. 职业：判断照片中人职业, 如果在办公室，则为白领
4. 表情：描述图片中人的表情。
5. 背景：详细描述背景情况，尽可能判断可能的地点，如公司、工厂、室外等。同时，说明背景中是否有人，如果有人，描述其动作。如果没有人则不输出"未见其他人"等描述
6. 戴眼镜：判断图片中人是否戴眼镜，只能填写"是"或"否"。
7. 是否遮挡：判断图片中是脸部是否有遮挡
8. 戴耳机: 明确判断图片中人是否戴耳机，只能填写“是”或“否”。
9. 戴口罩: 明确判断图片中人是否戴口罩，只能填写“是”或“否”。
10. 头发长短: 描述图片中人头发的长短情况，例如长发、短发等

以JSON格式输出分析结果，格式如下：
[
{"性别":"<男/女>","年龄":"<年龄>","职业":"<职业>","表情":"<表情>","背景":"<背景>","戴眼镜":"<是/否>", "脸部遮挡": "<是/否>"},
// 更多的照片的分析
]

如果照片中没有人脸，则对应输出结果为 ["照片中没有人脸"]

"""

    results = ark_vision_images(client, API_EP_ID, images, prompt, 0.01)

    print(results[0])
    print(results[1])

if __name__ == "__main__":
    main()
