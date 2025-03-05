import re
import io
import os
from openai import OpenAI
import logging



def ark_vision_images(client, item, prompt, endpoint):
    numbers = [re.search(r'_(\d+)\.jpg', url).group(1) for url in item if re.search(r'_(\d+)\.jpg', url)]
    if not numbers:
        logging.warning("No valid image URLs found in the input.")
        return None, None, None

    time_start = numbers[0]
    time_end = numbers[-1]
    logging.info(f"process {time_start} to {time_end}")

    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]
  
    try:
        completion = client.chat.completions.create(
            model=endpoint,
            messages=messages,
            temperature=0.01
        )

        return completion.choices[0].message.content, time_start, time_end

    except Exception as e:
        logging.error(f"Error while calling the API: {str(e)}")
        return None, time_start, time_end

def split_frames_into_batches(frames, batch_size):
    if not frames or not isinstance(frames, list):  
        logging.warning("Invalid or empty frames input.")
        return []
    return [frames[i:i + batch_size] for i in range(0, len(frames), batch_size)]


def handler(item, prompt, key, endpoint, batch_size):
    client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=key)
    batched_frames = split_frames_into_batches(item, batch_size=batch_size)
    buffer_vision = io.StringIO()
    for frames in batched_frames:
        tag, time_start, time_end = ark_vision_images(client, frames, prompt, endpoint)
        if tag is None and time_start is None and time_end is None:
            logging.warning(f"Invalid items: {item}")
        elif tag is None:
            logging.warning(f"{time_start} 毫秒 - {time_end} 毫秒: 无法判断分析结果")
        elif "1" in tag:
            interrupts = f"{time_start} 毫秒 - {time_end} 毫秒出现双录视频未录或黑屏现象"
            logging.info(interrupts)
            buffer_vision.write(interrupts)
            buffer_vision.write("\n")
        else:
            logging.info(f"{time_start} 毫秒 - {time_end} 毫秒正常")
    print(buffer_vision.getvalue())   



image_urls = [
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_7667.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_15335.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_23002.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_30670.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_38338.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_46005.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_53673.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_61340.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_69008.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_76676.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_84343.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_92011.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_99678.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_107346.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_115014.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_122681.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_130349.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_138017.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_145684.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_153352.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_161019.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_168687.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_176355.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_184022.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_191690.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_199357.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_207025.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_214693.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_222360.jpg",
    "https://pub-kylin.tos-cn-beijing.volces.com/cfitc/ff7c590d-2de7-40a2-8f30-968314cd631b/test-video-3_230028.jpg"
]

prompt = """你需要分析一组图片，任务是如果有超过2张图片中没人、或为单一背景色，或为黑屏，则回复1，反之回复0。

分析每张图片时，请注意以下几点：
1. 如果图片中没有人物，符合条件。
2. 如果图片是单一背景色（例如全白、全黑、全蓝等），符合条件。
3. 如果图片是黑屏，也符合条件。

逐一检查这些图片，统计符合条件的图片数量。如果这个数量超过2张，回复1，否则回复0。直接给出最终结果，无需任何额外的解释或说明。
"""

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

handler(image_urls, prompt, API_KEY, API_EP_ID, 10)

#ark_vision_images(image_urls)
