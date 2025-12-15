import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你的任务是分析催收对话文本，完成标签打标并输出指定字段内容。首先请阅读以下待分析的催收对话文本：
<催收对话文本>
{{催收对话文本}}
</催收对话文本>

### 标签定义及规则
请严格按照以下定义对对话内容进行打标（标签共四个：重大投诉、轻生、承诺还款、拒绝还款）：
1. **重大投诉**：提及上报/投诉至金融监督管理局、中国人民银行（12363）、12378、金融办、互联网金融协会、监管机构等，排除语音助手留言场景
2. **轻生**：客户/三方提及轻生倾向（如自杀、跳楼、想死、活不下去等），或反馈客户因轻生/自杀/自残正在治疗恢复的情形（参考示例："我已经想自杀了你们不要逼我"等）
3. **承诺还款**：客户本人明确答应还款（需同时包含具体时间和金额），且对话中无重大投诉或轻生内容
4. **拒绝还款**：客户本人明确表达拒绝还款（如"我不还了/一分钱都不会还"），且对话中无重大投诉或轻生内容

### 输出字段要求
请基于对话内容，输出以下9个字段（参考示例格式，确保内容贴合对话实际）：
- 催收结果：从四个标签中选择匹配项（若有多个标签，按"重大投诉轻生承诺还款/拒绝还款"优先级选择）
- 催收结果-总概：对催收结果的具体描述（如重大投诉需说明投诉对象、轻生需说明具体表述等）
- 逾期原因：提炼对话中客户提及的逾期原因（多个原因用顿号分隔）
- 逾期原因-总概：对逾期原因的详细说明
- 风险：提炼对话中存在的风险点（如监管投诉、法律诉讼等，多个风险用顿号分隔）
- 风险-总概：对风险点的详细说明
- 还款时间：明确客户承诺的还款时间（若无则填"未明确还款时间"）
- 还款时间-总概：对还款时间的补充说明（若无则填对应解释）
- 催记内容：对整个催收对话的总结（需包含客户态度、核心诉求、风险点等关键信息）

### 操作流程
1. 首先在<思考>标签中详细分析对话内容，说明每个标签的匹配情况（符合/不符合及依据），同时梳理逾期原因、风险点、还款时间等信息
2. 然后在<结果>标签中按要求输出9个字段内容，字段值用双引号包裹，每个字段单独一行

<思考>
[在此处详细分析对话内容：
1. 逐一判断是否符合四个标签的定义（说明符合/不符合的具体依据）
2. 梳理逾期原因、风险点、还款时间等关键信息
3. 确定最终打标结果及各字段内容的依据]
</思考>

<结果>
"催收结果": "[填写匹配的标签]"
"催收结果-总概": "[填写催收结果的详细描述]"
"逾期原因": "[填写提炼的逾期原因，多个用顿号分隔]"
"逾期原因-总概": "[填写逾期原因的详细说明]"
"风险": "[填写提炼的风险点，多个用顿号分隔]"
"风险-总概": "[填写风险点的详细说明]"
"还款时间": "[填写具体还款时间或'未明确还款时间']"
"还款时间-总概": "[填写还款时间的补充说明]"
"催记内容": "[填写对催收对话的总结]"
</结果>
"""

API_KEY = os.environ.get("ARK_API_KEY")
ARK_API_ENGPOINT_ID = os.environ.get("ARK_API_ENGPOINT_ID")

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
        with open(filepath, 'r', encoding='utf-8') as fp:
            content = fp.read()
        prompt = original_prompt.replace("{{催收对话文本}}", content)

       # print(prompt)
    except FileNotFoundError:
        logging.error(f"错误: 文件 {filepath} 未找到。")
    except Exception as e:
        logging.error(f"发生未知错误: {e}")



    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=ARK_API_ENGPOINT_ID,
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=16000
    )

    message = completion.choices[0].message.content
    usage = completion.usage
    logging.info(f"文件 {filepath} 的使用情况: {usage}")

@log_time
def main(folder):
    asr_files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.getsize(os.path.join(folder, f)) > 0
    ]

    logging.info(f"总共发现 {len(asr_files)} 个 ASR 文件待处理")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(execute, path): path for path in asr_files}

        for future in as_completed(futures):
            filepath = futures[future]
            try:
                future.result()
                logging.info(f"文件处理完成: {filepath}")
            except Exception as e:
                logging.error(f"文件处理失败 {filepath}: {e}")


if __name__ == "__main__":
    folder = "cost"
    main(folder)
