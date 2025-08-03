import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
import threading
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
    你是一名催收管理员，需要处理提供的催收对话。你的任务是分析整体对话，为“speaker - x”分配“客户”或“坐席”的角色，然后将原对话中的“speaker - x”替换为分配后的角色，最后输出替换后的JSON数组。
    
    以下是催收对话：
    <催收对话>
    {{COLLECTION_DIALOG}}
    </催收对话>

在分析角色时，可依据以下规则：

    1. 主动介绍产品，提及账单、询问贷款意愿、提供借款方式和减免政策等与贷款业务相关信息的一方通常为坐席；对贷款时间、意愿、方式等提出疑问或说明自身困难情况的一方通常为客户。
    2. 仔细分析对话，如果对话中只有 “speaker - 1”和“speaker - 2”，则分别为“客户”或“坐席”，将对应的speaker - x 全部修改为对应的“客户”或“坐席”
    3. 如果对话中，有“speaker - 3”，则判断“speaker - 3的类型，如果是电话语音提示，则标记为”语音提示“

# 输出格式
只输出替换角色后的JSON数组，不做额外的输出或解释。
"""

API_KEY = os.environ.get("ARK_API_KEY")

models = [os.environ.get("ARK_API_ENGPOINT_ID_1")]


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
            json.dump(json_obj, file, ensure_ascii=False, indent=2)
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
