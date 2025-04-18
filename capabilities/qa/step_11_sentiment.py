import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
import threading
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一名催收管理员，负责处理提供的催收对话。你的任务是对客服和客户的每一句话进行情感分析，并将分析结果添加到对应的JSON结构语句中，最后输出修改后的JSON数组。
请仔细阅读以下催收对话：
<催收对话>
{{COLLECTION_DIALOG}}
</催收对话>
在进行情感分析时，请参考以下按情绪强度从平缓到激烈排列的五个双字情感词语：
1. 平静（情绪稳定、无波澜）
2. 不满（轻微不快，有所抱怨）
3. 焦躁（心烦意乱，略显急切）
4. 激动（情绪高涨，带有强烈反应）
5. 愤怒（强烈的不满和敌意，情绪爆发）
对于对话中的每一句话，仔细分析，给出分析结果，然后在对应的JSON结构语句中添加 "sentiment": <分析结果> 。分析结果只能是“平静”、“不满”、“焦躁”、“激动”或“愤怒”。
{
    "role": "客服",
    "time": "string",
    "text": "string",
    "sentiment": "平静"
}
最后，请输出修改后的JSON数组，不做额外的输出或解释。
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
        target = filepath.replace("role", "sentiment")
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
