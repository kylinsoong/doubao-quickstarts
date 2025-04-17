import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
import threading
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
    你是一名催收管理员，需要处理提供的催收对话。你的任务是分析整体对话，为“speaker - 1”和“speaker - 2”分配“客户”或“客服”的角色，然后将原对话中的“speaker - 1”和“speaker - 2”替换为分配后的角色，最后输出替换后的JSON数组。
    
    以下是催收对话：
    <催收对话>
    {{COLLECTION_DIALOG}}
    </催收对话>

在分析角色时，可依据以下规则：

    1. 主动提及催收账单、询问还款意愿、提供还款方式和减免政策等与催收业务相关信息的一方通常为客服；对还款时间、方式等提出疑问或说明自身还款困难情况的一方通常为客户。
    2. 仔细分析对话，判断“speaker - 1”和“speaker - 2”分别为“客户”或“客服”
    3. 如果对话中，有“speaker - 3”，则判断“speaker - 3”为“客户”或“客服”，将原对话中“speaker - 3”替换

# 输出格式
只输出替换角色后的JSON数组，不做额外的输出或解释。
"""

API_KEY = os.environ.get("ARK_API_KEY")

models = [os.environ.get("ARK_API_ENGPOINT_ID_1"), os.environ.get("ARK_API_ENGPOINT_ID_2"), os.environ.get("ARK_API_ENGPOINT_ID_3")]


def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

def execute(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            collection_dialog = json.load(file)
        prompt = original_prompt.replace("{{COLLECTION_DIALOG}}", json.dumps(collection_dialog, ensure_ascii=False))

    except FileNotFoundError:
        logging.error(f"错误: 文件 {filepath} 未找到。")
        return None, None
    except json.JSONDecodeError:
        logging.error(f"错误: 无法解析 {filepath} 中的JSON数据。")
        return None, None
    except Exception as e:
        logging.error(f"发生未知错误: {e}")
        return None, None

    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=random.choice(models),
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=16000
    )

    message = completion.choices[0].message.content
    usage = completion.usage
    if message and usage:
        target = filepath.replace("input", "role")
        try:
            json_obj = json.loads(message)
        except json.JSONDecodeError:
            json_obj = message
        with open(target, 'w', encoding='utf-8') as file:
            json.dump(json_obj, file, ensure_ascii=False)
        logging.info(f"文件 {filepath} 的使用情况: {usage}")

@log_time
def main(folder):
    # 获取文件夹中所有的JSON文件
    json_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.json')]
    threads = []
    for filepath in json_files:
        logging.info(f"Process {filepath}")
        #thread = threading.Thread(target=execute, args=(filepath))

        thread = threading.Thread(target=execute, args=(filepath,))
        threads.append(thread)
        thread.start()

        if len(threads) == 10:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()


if __name__ == "__main__":
    folder = "input"
    main(folder)
