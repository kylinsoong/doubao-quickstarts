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

prompt = """
你需要分析一个视频，任务是检测视频的连续性，以结构化 JSON 格式输出结果。

分析视频画面：
1. 如果画面超过 3 秒钟是卡顿的，则视频不连续
2. 如果画面中一直没有人物，则视频不连续
3. 如果画面是单一背景色（例如全白、全黑、全蓝等），则视频不连续
4. 如果画面是黑屏，则视频不连续

如果视频不连续，记录视频出现不连续的时间段，以及不连续的原因，如果视频是连续的，则值输出连续性标记，不需要记录时间段和原因

输出格式：
{"consistence": true/false, "notes": ["<不连续时间段> <原因>", "//如果有更多不连续时间段，依次记录"]}
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
            "type":"enabled"
        }
    )

    return completion.choices[0].message.content, completion.usage

@log_time
def main():
    video_url = "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/103.mp4"
    summary, usage = analyze_video(video_url)
    json_obj = json.loads(summary)
    with open("vlm.json", 'w') as file:
        json.dump(json_obj, file, ensure_ascii=False)
    print(usage)


if __name__ == "__main__":
    main()

