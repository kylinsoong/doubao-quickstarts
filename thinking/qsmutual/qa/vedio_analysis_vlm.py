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
你是一名视频字幕核对助手，负责核对视频声音和字幕是否同步。具体任务是结合ASR提取的JSON结构化的视频字幕，对比分析视频画面中的字幕时间是否和JSON结构化的视频字幕的开始时间和结束时间同步，并记录分析结果。

如下ASR 字幕示例，字幕 "我是北京市第六医院妇产科大夫" 开始时间是 4.8 秒，结束的时间是 7.46 秒。 

<ASR 字幕示例>
  {
    "start_time": 4.8,
    "end_time": 7.46,
    "text": "我是北京市第六医院妇产科大夫"
  }
</ASR 字幕示例>



首先，请仔细阅读以下ASR提取的JSON结构化的视频字幕：
<ASR_JSON_subtitles>
{{ASR_JSON_SUBTITLES}}
</ASR_JSON_subtitles>
接下来，请仔细分析视频画面中的字幕，按照以下步骤进行：
1. 逐一对视频画面中的字幕与JSON结构化字幕进行匹配。
2. 对比每一条匹配字幕的开始时间和结束时间。
3. 若开始时间和结束时间一致或在可接受的误差范围内（如±0.5秒），则判定为同步；否则判定为不同步。
4. 记录每一条字幕的核对结果，如果不同步，在结果 "notes" 字段说明视频画面字幕的延迟出现，还是提前出现，并记录具体的时间，。

请结合JSON结构化的视频字幕仔细分析视频，然后逐条修改<ASR_JSON_subtitles> 中字幕，增加 "vlm" 属性记录结果

输出格式为 JSON，不做额外解释，如下为输出示例：
[
  {
    "start_time": 4.8,
    "end_time": 7.46,
    "text": "我是北京市第六医院妇产科大夫",
    "vlm": {"是否同步":"<是/否>", "notes":"<视频画面字幕的延迟出现/提前出现> X 秒"}
  }
]

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
    video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/020.mp4"
    summary, usage = analyze_video(video_url)
    #print(summary)
    json_obj = json.loads(summary)
    with open("vlm.json", 'w') as file:
        json.dump(json_obj, file, ensure_ascii=False)
    print(usage)


if __name__ == "__main__":
    main()

