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
分析图片，提取图片中门头照名称

# 要求
1. 如果图片中有多门头照名称，分析照片中主门头照，并提取门头照名称
2. 如果门头照名称有副标题，提提取补充信息，记作门店信息
3. 从字体、颜色、图案等维度分析门头照招牌设计，总结设计特点，记作招牌设计
4. 分析主门头照周边环境信息，记作周边环境
5. 分析照片，给照片打标签，记作：标签1，标签2，...

直接以 JSON 格式输出，只输出 JSON 结果，不做额外的解释或标记

输出结果符合严格JSON 语法，示例如下：

{"店铺名称": "<门头照名称>", "详细信息": "<门店信息>", "招牌设计": "<招牌设计>", "周边环境": "<周边环境>", "标签": ["<标签1>", "<标签2>", ...]}

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
        target = os.path.join("results", f"{id}.json")
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
