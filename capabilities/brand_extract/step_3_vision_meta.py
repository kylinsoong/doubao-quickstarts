import os
import requests
import time
import uuid
import json
import logging
from volcenginesdkarkruntime import Ark
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt = """
分析图片，提取照片一般属性，提取文件名、文件类型、文件大小、创建日期、修改日期，图像大小、图像DPI、颜色模式，以JSON格式输出:
{"文件名":"<文件名>", "文件类型":"<文件类型>", "文件大小":"<文件大小>", "创建日期":"<创建日期>", "修改日期":"<修改日期>", "图像大小":"<图像大小>", "图像DPI":"<图像DPI>", "颜色模式":"<颜色模式>"}
"""

def execute(id, url):
    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url":  url}
                    },
                ],
            }
        ],
    )

    message = completion.choices[0].message.content
    if message:
        target = os.path.join("results", f"meta-{id}.json")
        with open(target, 'w', encoding='utf-8') as file:
            file.write(message)

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@log_time
def main(json_path, max_workers=10):
    data = load_json(json_path)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for item in data:
            id = item['id']
            name = item['name']
            url = item['url']
            futures.append(executor.submit(execute, id, url))
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Task failed: {e}")

if __name__ == "__main__":
    json_path = "object_urls.json"
    main(json_path, max_workers=8)
