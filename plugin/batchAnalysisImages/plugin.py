from runtime import Args
from typings.videoframesanalysis.videoframesanalysis import Input, Output
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



"""
Each file needs to export a function named `handler`. This function is the entrance to the Tool.

Parameters:
args: parameters of the entry function.
args.input - input parameters, you can get test input value by args.input.xxx.
args.logger - logger instance used to print logs, injected by runtime.

Remember to fill in input/output in Metadata, it helps LLM to recognize and use tool.

Return:
The return data of the function, which should match the declared output parameters.
"""
def handler(args: Args[Input])->Output:

    items = args.input.items
    prompt = args.input.prompt
    key = args.input.key
    endpoint = args.input.endpoint
    batch_size = args.input.batch_size

    client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=key)
    batched_frames = split_frames_into_batches(items, batch_size=batch_size)
    results = []

    for frames in batched_frames:
        tag, time_start, time_end = ark_vision_images(client, frames, prompt, endpoint)
        if tag is None and time_start is None and time_end is None:
            logging.warning(f"Invalid images: {frames}")
        elif tag is None:
            logging.warning(f"{time_start} 毫秒 - {time_end} 毫秒: 无法判断分析结果")
        elif "1" in tag:
            interrupts = f"{time_start} 毫秒 - {time_end} 毫秒出现双录视频未录或黑屏现象"
            logging.info(interrupts)
            results.append(interrupts)
        else:
            logging.info(f"{time_start} 毫秒 - {time_end} 毫秒正常")

    if len(results) == 0:
        results.append("视频分析显示该双录视频是连续的")

    return {"message": results}::q!
