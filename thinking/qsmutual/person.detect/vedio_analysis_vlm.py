import os
import json
from volcenginesdkarkruntime import Ark
import time
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
识别与分析视频内容，告诉我视频中有没有人出现，结果以json格式返回，json示例：{"has_human": 1  ## 1有人 0没人}
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

    # DO NOT WORK
    video_url = "https://baoxian-crm.oss-accelerate.aliyuncs.com/momo_tracker_videos/1750774970_motion_video_6c69d36c-29ab-4a4e-91bb-82292229363d_1913753014424911873_1750773216.mp4"
    #video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/1750773216.mp4"
    #video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/1750773216_copy.mp4"
    #video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/copy.mp4"

    # WORK
    #video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0004/003.mp4"
    #video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/1750773217.mp4"    
    #video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/1750773218.mp4"    

    summary, usage = analyze_video(video_url)
    print()
    print(summary)
    print()
    print(usage)


if __name__ == "__main__":
    main()

