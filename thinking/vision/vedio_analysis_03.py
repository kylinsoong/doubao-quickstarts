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
                    {"type": "text", "text": "仔细分析视频，分时间段说明视频内容"},
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
        ]
    )

    return completion.choices[0].message.content, completion.usage

@log_time
def main():
    video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0004/001.mp4"
    summary, usage = analyze_video(video_url)
    print(summary)
    print(usage)


if __name__ == "__main__":
    main()

