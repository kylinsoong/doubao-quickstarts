import os
from volcenginesdkarkruntime import Ark
import time

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

system_prompt = """
You should first think about the reasoning process in the mind and then provide the user with the answer. The reasoning process is enclosed within <think> </think> tags, i.e. <think> reasoning process here </think>here answer

<think>
思考内容
</think>
回答内容
"""

prompt = """
你是一位智力游戏挑战专家，挑战找不同，仔细分析图片，找出两幅相似图片中的不同之处，找出的不同之处越多越好，记录不同之处，并进行简要解释说明

# 输出格式
1. <str>：<简要解释>
2. <str>：<简要解释>
3. <str>：<简要解释>
// 如果有更过不同，依次罗列

要求严格按照输出格式输出，不做额外解释
"""

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

def analyze_image(img_url):
    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",  
                "content": [  
                    {"type": "text", "text": prompt},  
                    {
                        "type": "image_url", 
                        "image_url": {"url":  img_url}
                    },
                ],
            }
        ]
    )

    return completion.choices[0].message.content, completion.usage

@log_time
def main():
    img_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/Spot_the_difference.png"
    summary, usage = analyze_image(img_url)
    print(summary)
    print(usage)


if __name__ == "__main__":
    main()

    

