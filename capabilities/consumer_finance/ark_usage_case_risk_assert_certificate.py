import os
import sys
import base64
from volcenginesdkarkruntime import Ark


API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

default_prompt = """
分析图片，提取图片中两类要素：
1. 身份识别三要素（姓名、身份证号、手机号），如果图片中有三要素，则提取，并一次标记为姓名、身份证好、手机号，如果某个要素没有，则标记为无
2. 资产证明要素，提取图片中购买年限、购买时间、购买产品名、购买金额

以 JSON 结果输出，不做额外解释，输出示例：
[
{"姓名": "<姓名>", "身份证号":"<身份证号>", "手机号":"<手机号>", "购买年限":"<购买年限>", "购买产品名":"<购买产品名>", "购买时间":"<购买时间>", "购买金额":"<购买金额>"},
//如果有多张图片一次输出
]
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
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/sample/1.jpg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/sample/2.jpg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/sample/3.jpg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/sample/4.jpg"}
                }
            ],
        }
    ]

    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=messages,
        temperature=0.01
    )

    return completion.choices[0].message.content



def main():
    check_environment_variables()
    results = do_inference()
    print(results)


if __name__ == "__main__":
    main()
