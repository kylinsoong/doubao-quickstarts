import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
from concurrent.futures import ThreadPoolExecutor
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一名催收管理员，需要根据提供的结构化催收分析结果（以JSON结构化方式保存），为催收客服进行画像。画像将从专业能力、催收效率、沟通技巧、意图掌控、情绪控制、应变能力这六个维度进行评估，并计算综合得分。
以下是结构化的吸收分析结果：
<结构化分析结果>
{{STRUCTURED_ANALYSIS_RESULT}}
</结构化分析结果>
各个维度的评估标准和打分方法如下：
### 专业能力
分析 JSON 对象 forms 子对象：
 - 如果 "客服是否完成催收" 属性值为 "是"，则直接得 5 分。
 - 若未完成催收，"客户姓名" 不为空得1 分，"产品名称" 不为空得1 分，"对话总结"不为空得1 分，"交互轮次" 超过 5次得1 分。注意专业能力满分 5 分，需将未完成催收情况下根据各项所得分数累加。

### 催收效率
分析 JSON 对象 results 子对象的 summary 对象属性：
 - 整体评级为“优秀”得 5分。
 - 整体评级为“合格”得 4分。
 - 整体评级为“一般”得 3分。
 - 整体评级为“差”得 2分。注意催收效率满分为5分，最低分为2分。

### 沟通技巧
分析 JSON 对象 complaint 子对象：
 - 如果 "投诉倾向" 属性值为 "是"，则得1分。
 - 若 "投诉倾向" 属性值为 "否"，分析 JSON 对象 huankuan 子对象：
    - "还款意愿" 属性值为“已还款”或“约定时间再谈”则得 5分。
    - "还款意愿" 属性值为“高风险”或“无还款意愿”得3分。
    - 若值为其它值得2分。注意沟通技巧满分为5分，最低分为1分。

### 意图掌控
分析 JSON 对象 complaint 子对象：
 - 如果 "风险总结" 部分风险低，则直接得5分。
 - 如果客服的主要意图达到，得4分。
 - 如果客服主要意图明确，则得3分。
 - 如果 "对话主题分布" 部分，客户主要意图占比超过 50%，则得2 分；客户主要意图占比超过 60%，则得1 分。注意，意图掌控满分 5 分，最低分 1 分。

### 情绪控制
分析 JSON 对象 sentiment_summary 子对象：
 - 如果 "情感变化责任方" 为“客服”，则得1分。
 - 如果 "情感变化责任方" 为“客户”，则得 3 分。
 - 如果 "情感变化责任方" 为“客户”，而且 "情感分析摘要" 中客服情绪稳定，则得5分。情绪控制满分 5 分，最低分 1 分。

### 应变能力
分析 JSON 对象 abnormals 子对象：
 - 如果发生异常、异常发生的责任方为客户，且客服保持平静，则得 5分。
 - 如果发生异常，且异常发生的责任方为客服，则得 1分。
 - 其他情况得3分。注意应变能力满分5分，最低分 1分。

### 综合得分
以上6个维度（专业能力、催收效率、沟通技巧、意图掌控、情绪控制、应变能力）得分的总和，总分30分。

请在仔细分析JSON 结构化催收分析结果，，然后按照以下JSON格式在输出客服画像结果，不过任何额外解释。
{"专业能力": int,"催收效率": int,"沟通技巧": int,"意图掌控": int,"情绪控制": int,"应变能力": int,"综合得分": int}
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
        prompt = original_prompt.replace("{{STRUCTURED_ANALYSIS_RESULT}}", json.dumps(collection_dialog, ensure_ascii=False))

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
        target = filepath.replace("figure_input", "figure")
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
    folder = "figure_input"
    main(folder)
