import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
from concurrent.futures import ThreadPoolExecutor
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一名情感分析师，任务是处理完成情感分析的催收对话。请仔细阅读以下催收对话（结构化 JSON 格式），对话已经完成了情感标记。
<催收对话>
{{COLLECTION_CONVERSATION}}
</催收对话>
情感标记按情绪强度从平缓到激烈排列的五个双字情感词语及其含义如下：
1. 平静（情绪稳定、无波澜）
2. 不满（轻微不快，有所抱怨）
3. 焦躁（心烦意乱，略显急切）
4. 激动（情绪高涨，带有强烈反应）
5. 愤怒（强烈的不满和敌意，情绪爆发）

请依据以上信息进行如下情感分析：
1. 情感分析摘要：描述客服和客户对话情感变化趋势，并说明在什么时间点客服或客户的对话内容引起的情感变化。
2. 情感变化责任方：分析情感趋向激烈画的的责任方是客服还是客户，如果没有出现焦躁、激动、愤怒，则标记为无
3. 情感变化关键对话：引用具体引起情感变化的语句，最多不超过三句，严格按照原始内容引用，格式为<客服/客户> <time> <string>。如果情感没有变化，则本部分为空。
4. 情绪变化关键词：分析情感发生变化时的对话，若情感发生变化，提取情绪变化关键词语，并统计该关键词出现次数，格式为 <词语1> <出现次数>, <词语2> <出现次数>。要求情绪变化关键词不能超过5个
5. 如果客服情感出现焦躁、激动、愤怒等标记，则给出改进建议。


请以JSON格式输出你的分析结果，不做过多解释，输出示例：
{"情感分析摘要":"string", "情感变化责任方":"客服/客户/无","情感变化关键对话":["客服/客户 <time> <string>", "客服/客户 <time> <string>"], "情绪变化关键词": ["<词语1> 出现次数", "<词语2> 出现次数", //如果有更多，依次罗列], "改进建议": ["建议 1"，"建议 2"，//如果有更多，依次罗列]}
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
        prompt = original_prompt.replace("{{COLLECTION_CONVERSATION}}", json.dumps(collection_dialog, ensure_ascii=False))

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
        target = filepath.replace("sentiment", "sentiment_summary")
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
