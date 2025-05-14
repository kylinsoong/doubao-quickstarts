import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

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
        return completion.choices[0].message.content, completion.usage
    except Exception as e:
        return e

prompt = """
分析婴儿胚胎发育照片，从医学角度提取一些数据，以结构化 JSON 格式输出
"""


images = [
"https://pub-kylin.tos-cn-beijing.volces.com/baby/6.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/baby/16.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/baby/20.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/baby/22.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/baby/32.jpg",
]

results = ark_vision_images(images, prompt, 0.01)

print(results[0])
