import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
import threading
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你的任务是对客服与客户的对话进行意图分析，具体涵盖分析客服的主要意图和次要意图、客户的主要意图、风险等级、关键信息点以及对话主题分布等方面。

以下是客服与客户的对话：
<dialogue>
{{DIALOGUE}}
</dialogue>

在进行分析时，请依照以下具体要求操作：
1. 认真剖析客服的发言，明确客服的主要意图和次要意图。若无法得出相应意图，则标记为“无”。
2. 仔细研读客户的发言，确定客户的主要意图。若无法得出该意图，同样标记为“无”。
3. 关键信息点指的是能够体现客服的主要意图、次要意图以及客户的主要意图的发言内容，要求直接引用客服或客户的原始语言。
4. 主题分布：分析整体上客服的主要意图、次要意图以及客户的主要意图在对话内容中所占的分布比例，这些分布比例相加需为100%。
5. 风险总结的格式为：<风险等级> <原因>。风险等级分为高、中、低三个等级。若客服的主要意图达成，则风险等级为低；若客服的主要意图未达成，但次要意图达成，则风险等级为中；若客服的主要意图和次要意图均未达成，则风险等级为高。

请以JSON结构化形式输出你的分析结果。JSON结构应包含以下字段：
{
    "客服主要意图": "string",
    "客服次要意图": "string",
    "客户主要意图": "string",
    "风险总结": ["<低/中/高>", "<原因>"],
    "关键信息点": [
        "客服发言", "客服发言", "客户发言"
    ],
    "对话主题分布": {
        "<客服主要意图>": "<百分比>",
        "<客服次要意图>": "<百分比>",
        "<客户主要意图>": "<百分比>"
    }
}
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
        prompt = original_prompt.replace("{{DIALOGUE}}", json.dumps(collection_dialog, ensure_ascii=False))

        #print(prompt)
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
        target = filepath.replace("role", "intent")
        with open(target, 'w', encoding='utf-8') as file:
            file.write(message)
        logging.info(f"文件 {filepath} 的使用情况: {usage}, resulsts: {target}")

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

        if len(threads) == 20:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()


if __name__ == "__main__":
    folder = "role"
    main(folder)
