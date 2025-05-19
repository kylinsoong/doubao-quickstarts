import os
import json
from volcenginesdkarkruntime import Ark
import time

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

prompt ="""
分析单人口播视频，提取口播字幕，字幕会在视频图像中下部，且随着视频推进，字幕在不停变化，要求：

1. 提取所有字幕，尽可能细化,分析不同画面间差异，只提取字幕
2. 每句字幕需要有对应的开始时间 start_time, 和结束时间 end_time，单位为妙，保持小数点后 2 位
3. 字幕不能重读，一个画面中的字幕不能提取两次或多次
4. 输出格式为 JSON 结构化格式，如下为一示例：


[
  {
    "start_time": 0.16,
    "end_time": 0.72,
    "text": "<str>"
  },
  {
    "start_time": 0.72,
    "end_time": 2.64,
    "text": "<str>"
  },
  // 更多口播
]

要求只输出 JSON 结构的字幕，不做过多解释
"""

def analyze_video(video_url: str):
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
                            "fps": 1.0,
                            "detail": "low"
                        }
                    },
                ],
            }
        ],
        thinking = {
            "type":"disabled"
        }
    )

    return completion.choices[0].message.content, completion.usage

@log_time
def main():
    video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0004/003.mp4"
    summary, usage = analyze_video(video_url)
    json_obj = json.loads(summary)
    with open("vlm.json", 'w') as file:
        json.dump(json_obj, file, ensure_ascii=False)
    print(usage)


if __name__ == "__main__":
    main()

