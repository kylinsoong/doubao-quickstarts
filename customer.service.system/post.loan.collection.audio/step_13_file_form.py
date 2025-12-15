import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
from concurrent.futures import ThreadPoolExecutor
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一名催收管理员，需要处理提供的JSON结构化的催收对话。你的任务是分析整体客服和客户对话，理解并归纳其中的关键点，填写工单。
以下是催收对话的JSON数据：
<催收对话>
{{COLLECTION_DIALOGUE}}
</催收对话>
工单需以JSON结构化格式输出，各字段的填写要求如下：
- "客户姓名": 通过客服在对话的开始确认的客户姓名来记录。
- "交互轮次": 只有客服和客户有互动才算一个轮次，统计客服和客户对话的交互轮次。
- "对话时长": 对话的JSON输入中有time属性，该属性代表当前对话开始的时间和结束的时间（如0.24 - 1.01即当前对话从0.24秒开始，到1.01秒结束），分析最后一句对话，获取整体对话的时长。
- "产品名称": 客服会给客户说明贷款产品的名称，例如桔多多、桔享花，记录该产品名称，如果对话内容产品书写有误，则更正。
- "对话总结": 概述总结客服和客户对话的内容，回答需丰富、全面。
- "客服是否完成催收": 分析整体对话，如果客户确定会还款，则标记是，否则标记否。
- "下次跟进": 分析整体对话，给出是否需要跟进，以及跟进的时间。

要求输出符合要求的JSON格式的工单，不做任何额外解释。
{
"客户姓名": "",
"交互轮次": "",
"对话时长": "",
"产品名称": "",
"对话总结": "",
"客服是否完成催收": "",
"下次跟进": ""
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
        target = filepath.replace("role", "form")
        with open(target, 'w', encoding='utf-8') as file:
            file.write(message)
        logging.info(f"文件 {filepath} 的使用情况: {usage}, resulsts: {target}")

@log_time
def main(folder):
    json_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.json')]
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(execute, filepath) for filepath in json_files]
        for future in futures:
            future.result()

if __name__ == "__main__":
    folder = "role"
    main(folder)
