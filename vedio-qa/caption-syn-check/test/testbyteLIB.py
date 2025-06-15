import os
from byteLIB import ByteTOS
from byteLIB import ByteVideoASR
from byteLIB import ByteVLM

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket = os.getenv('TOS_BUCKET')

appid = os.getenv("X_API_APPID")
access_token = os.getenv("X_API_TOKEN")

api_key = os.environ.get("ARK_API_KEY")
model = os.environ.get("ARK_API_ENGPOINT_ID")


original_prompt ="""
你是一名视频字幕核对助手，负责核对视频声音和字幕是否同步。具体任务是结合ASR提取的JSON结构化的视频字幕，对比分析视频画面中的字幕时间是否和JSON结构>化的视频字幕的开始时间和结束时间同步，并记录分析结果。

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

tos = ByteTOS(ak=ak, sk=sk, endpoint=endpoint, region=region, bucket=bucket)
asr = ByteVideoASR(appid=appid, access_token=access_token)
vlm = ByteVLM(api_key=api_key,model=model)

obj_key = "qsmutual/021.mp4"
url = tos.generate_signed_url(obj_key)

asr_results = asr.process(url)

prompt = original_prompt.replace("{{ASR_JSON_SUBTITLES}}", asr_results)

final_results = vlm.process(prompt=prompt,video_url=url,thinking="disabled")

print(final_results)

