import os
from volcenginesdkarkruntime import Ark
import logging
import json

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")
default_batch_size = 10
vision_batch_size = int(os.getenv("LLM_VISION_BATCH_SIZE", default_batch_size))

client = Ark(api_key=API_KEY)

def load_frames():
    frame_list = []

    return frame_list


def ark_vision_images(item):

    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]

    try:
        completion = client.chat.completions.create(
            model=API_EP_ID,
            messages=messages,
            temperature=0.01
        )

        return completion.choices[0].message.content

    except Exception as e:
        logging.error(f"Error while calling the API: {str(e)}")
        return None


def split_frames_into_batches(frames, batch_size=10):
    if not frames or not isinstance(frames, list):
        logging.warning("Invalid or empty frames input.")
        return []
    return [frames[i:i + batch_size] for i in range(0, len(frames), batch_size)]

url_list = load_frames()

new_url_list = list(map(lambda x: x.replace("ivolces.com", "volces.com"), url_list))
batched_frames = split_frames_into_batches(new_url_list, batch_size=vision_batch_size)


prompt = """
你将执行一个分析一组图片的任务，任务的结果是判断图片中是否有给卡车加油，结果有两种：正常加油和没有加油。并且需要按照特定的判断逻辑得出结论，最后以JSON格式输出
结果。

下面是判断逻辑：
1. 如果有1张及以上图片显示看到一个戴着安全帽、身穿工作服的人拿着类似加油管的物件，站在一辆车旁边，且车是禁止的，则正常加油,否则显示没有加油
2. 在得出结论后，需要简单总结得出该结论的原因, 且结论出不出现图片字样，例如”图片中显示“，则描述为”视频中显示“。
3. 在结论部分简单描述工作人员一幅颜色，卡车颜色，是否佩戴头盔等

以JSON格式输出结果，格式为{"result":"正常加油/没有加油", "reason":"判断的原因"}。
"""

temperature = 0.1

#results = ark_vision_images(frames, prompt, temperature)
#print(results)

for item in batched_frames:
    results = ark_vision_images(item)
    results_json = json.loads(results)
    if results_json.get("result") == "正常加油":
        print(results)
