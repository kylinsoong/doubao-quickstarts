import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
from concurrent.futures import ThreadPoolExecutor
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一名数据分析师，任务是处理完成情感分析的催收对话，生成客服和客户情感变化的 echarts Stacked Line Chart，横坐标为时间，纵坐标为情绪分。
请仔细阅读以下以 JSON 结构化形式呈现的催收对话：
<催收对话>
{{COLLECTION_DIALOGUE}}
</催收对话>
情感分析结果对催收对话的标记有 5 种，分别代表的情绪分范围为 1 - 5：
- 平静: 5
- 不满: 4 
- 焦躁: 3
- 激动: 2
- 愤怒: 1
从对话中提取时间和对应的情绪分，例如，若对话中有如下内容：
{
    "role": "客服",
    "time": "0.11 - 1.25",
    "text": "string",
    "sentiment": "焦躁"
}
则横坐标为时间，取该时间段的起始值 0.11，纵坐标为情绪分 3。
你的最终输出应为 html 格式的 echarts 脚本。
请输出html 代码，对代码不做任何解释。
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
        prompt = original_prompt.replace("{{COLLECTION_DIALOGUE}}", json.dumps(collection_dialog, ensure_ascii=False))

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
        target = filepath.replace("sentiment", "sentiment_chart")
        target = target.replace(".json", ".html")
        with open(target, 'w', encoding='utf-8') as file:
            file.write(message)
        logging.info(f"文件 {filepath} 的使用情况: {usage}, resulsts: {target}")

@log_time
def main(folder):
    # 获取文件夹中所有的JSON文件
    json_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.json')]
    # 创建线程池，最大线程数为 20
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交任务到线程池
        futures = [executor.submit(execute, filepath) for filepath in json_files]
        # 等待所有任务完成
        for future in futures:
            future.result()

if __name__ == "__main__":
    folder = "sentiment"
    main(folder)
