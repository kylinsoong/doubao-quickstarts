import os
import time
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

@log_time
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
            thinking = {
                "type":"disabled"
            },
            temperature=temperature,
            max_tokens=16000
        )
        return completion.choices[0].message.content, completion.usage
    except Exception as e:
        return e

prompt = """
你的任务是分析两张人脸图片，判断两张图片是否在同一个场景环境中。

注意：
1. 两张人脸可能在同一个环境，但是在不同时间
2. 两张人脸可能在同一个环境的不同角度
3. 可根据场景环境中文字或物体是否相同来判断是否在同一个环境

以JSON 结构输出结果，格式如下：

{"是否在同一个环境":"<是/否>", "原因":"解释判断的原因"}
"""


images = [
"https://pub-kylin.tos-cn-beijing.volces.com/8769/1001.jpeg",
"https://pub-kylin.tos-cn-beijing.volces.com/8769/1008.jpeg",
]

results = ark_vision_images(images, prompt, 0.01)

print(results[0])
print(results[1])
