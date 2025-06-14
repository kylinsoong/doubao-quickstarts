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

original_prompt ="""
你是一名HR助手，分析面试视频，给面试人进行打分。具体任务是结合ASR提取的JSON结构化的语音字幕，结合字幕和视频中图像进行分析。

如下ASR 字幕示例，字幕 "展现自己的价值" 开始时间是 165.16 秒，结束的时间是 166.54 秒。 

<ASR 字幕示例>
  {
    "start_time": 165.16,
    "end_time": 166.54,
    "text": "展现自己的价值"
  }
</ASR 字幕示例>

# 任务
首先，请仔细阅读以下ASR提取的JSON结构化的视频字幕：
<ASR_JSON_subtitles>
{{ASR_JSON_SUBTITLES}}
</ASR_JSON_subtitles>

其次，完成下列所有认为
1. 面试人整体表现总结：结合面试人语音字幕和视频图像给出面试人整体表现表现总结
2. 面试人表现不佳的问题：根据视频时序，结合面试人语音字幕和视频图像, 分析找出面试人表现不佳的问题回答并记录，记录中包括时间点、回答的原文，以及为什么不佳原因总结；如果有多个依次记录，例如 [{"时间点":"<str>",  "回答原文":"<str>", "不佳原因":"<str>"}, // 如果有更多表现不佳，依次罗列]



# 输出格式
以结构化 JSON 格式输出，不做额外的解释。
输出示例：
{"整体总结": <str>, "表现不佳": [{"时间点":"<str>",  "回答原文":"<str>", "不佳原因":"<str>"}, // 如果有更多表现不佳，依次罗列]}

"""

def analyze_video(video_url: str):
    if not API_KEY or not API_EP_ID:
        raise ValueError("Missing ARK_API_KEY or ARK_API_ENGPOINT_ID environment variables")

    with open("asr.json", 'r', encoding='utf-8') as file:
        collection_dialog = json.load(file)

    prompt = original_prompt.replace("{{ASR_JSON_SUBTITLES}}", json.dumps(collection_dialog, ensure_ascii=False))


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
                            "fps": 0.5,
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
    video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/201.mov"
    summary, usage = analyze_video(video_url)
    #print(summary)
    json_obj = json.loads(summary)
    with open("vlm.json", 'w') as file:
        json.dump(json_obj, file, ensure_ascii=False)
    print(usage)


if __name__ == "__main__":
    main()

