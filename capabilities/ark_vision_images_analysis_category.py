import os
import sys
import base64
from volcenginesdkarkruntime import Ark


API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

default_prompt = """你将对提供的图片进行分类、标记并根据图片类别提取特定内容。以下是图片内容：
<pictures>
{{PICTURES}}
</pictures>
不同图片类别有如下的分类、标记和内容提取要求：
1. 如果图片识别类别为“借呗额度管理”，则将图片分类为“jiebei”，提取总额度和可用额度，分别以 jb_total_amount 和 jb_remain_amount 标记，并以 {"scene": "jiebei","jb_total_amount":"","jb_remain_amount":} 格式输出。
2. 如果图片识别类别为“芝麻信用”，则将图片分类为“zhima”，提取芝麻信用分，以zhima_score标记，并以 {"scene": "zhima","zhima_score":""} 格式输出。
3. 如果图片识别类别为“住房公积金账户明细”，则图片类型为“gjjInfo”，标记"is_scene_valid": "1",提取手机系统时间，标记为phoneTime，提取所有汇缴的日期和汇缴的金额，并以{"is_scene_valid":"1","gjjInfo":["gjjOcrDate":"","gjjOcrAmt":""],"phoneTime":""} 格式输出。
4. 如果图片不是任何合法的业务场景类型，属于无效图片，则将图片分类为“null”，并以 {"scene": null} 格式输出。

你需要对每张图片进行上述操作，并以JSON格式返回结果。JSON结果的格式应为：
[
    {
        "scene": "jiebei",
        "jb_total_amount": "对应总额度",
        "jb_remain_amount": "对应可用额度"
    },
    {
        "scene": "zhima",
        "zhima_score": "对应芝麻信用分"
    },
    {
        "is_scene_valid": "1",
        "gjjInfo": [
          {
            "gjjOcrDate": "对应汇缴的日期，格式为19700101",
            "gjjOcrAmt": "对应汇缴的金额"
          },
          // 如果有更多的汇缴条目，按照上述格式列出所有汇缴条目
        ],
        "phoneTime": "对应手机系统时间"
    },
    {
        "scene": null 
    },
    // 如果有更多图片，按照上述格式根据图片分类依次添加
]
现在开始对图片进行分类、标记和内容提取操作。
"""

prompt = os.getenv("LLM_VISION_USER_PROMPT", default_prompt)

def check_environment_variables():
    if not API_KEY or not API_EP_ID:
        print("One or more required environment variables are not set. The program will exit.")
        sys.exit(1)


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def do_inference():
    client = Ark(api_key=API_KEY)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://qifu.tos-cn-beijing.volces.com/1.png"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://qifu.tos-cn-beijing.volces.com/2.png"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://qifu.tos-cn-beijing.volces.com/3.png"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://qifu.tos-cn-beijing.volces.com/4.png"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://qifu.tos-cn-beijing.volces.com/5.png"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://qifu.tos-cn-beijing.volces.com/6.jpg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://qifu.tos-cn-beijing.volces.com/7.jpg"}
                },
            ],
        }
    ]

    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=messages,
        temperature=0.5
    )

    return completion.choices[0].message.content



def main():
    check_environment_variables()
    results = do_inference()
    print(results)


if __name__ == "__main__":
    main()
