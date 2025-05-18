import os
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
分析单人口播视频，提取口播字幕，字幕会在口播视频图像中，要求：

1. 每个包括独立图像画面的字幕为独立的一句话
2. 每句话需要记录对应的时间间隔
3. 输出格式为 JSON 结构化格式，如下为一示例：


[
  {
    "time": "0.0 - 5.19",
    "text": "大家好，我是张医生"
  },
  {
    "time": "5.47 - 11.15",
    "text": "今天我给大家介绍过度运动带来的危害"
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
                            "fps": 2.0,
                            "detail": "low"
                        }
                    },
                ],
            }
        ],
    )

    return completion.choices[0].message.content, completion.usage

@log_time
def main():
    video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0004/003.mp4"
    summary, usage = analyze_video(video_url)
    print(summary)
    print(usage)


if __name__ == "__main__":
    main()

