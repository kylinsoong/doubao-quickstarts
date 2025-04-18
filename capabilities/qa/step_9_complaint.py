import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
import threading
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一位经验丰富且眼光敏锐的客户投诉倾向精准分析师，你的任务是通过研究客服与客户的交流细节，准确判断客户是否存在投诉倾向。
请仔细阅读以下客服与客户的对话内容：
<对话内容>
{{input}}
</对话内容>
在分析对话时，请遵循以下要求：
1. 全面且深入地理解对话内容，着重留意“客户”使用的语气、措辞和表达方式，深度剖析“客户”阐述问题的频率与严重程度。
2. 根据对话内容重点分析客户是否存在投诉、举报、报警倾向。投诉倾向的例子如下：
    - 我要通过银监会、网络曝光、互联网金融协会、黑猫平台、银监会、报警、等方式投诉你们  
    - 表示已经录音、索要工号、索要投诉电话并表明要投诉的意图
3. 依据客户对话结束时的最终表述，准确判断其情绪状态为愤怒、不满或者仅仅是提出疑问。若明确提及投诉，则判定为有投诉倾向，如果在对话过程中，通过坐席的安抚，客户不再说投诉了，则判定为不投诉。
4. 始终依据客户对话结束时的情绪与表述，来判断其是否具有投诉倾向，禁止主观臆断。

请只专注于客户投诉倾向意向的识别，仅根据给定的对话内容做出判断，严禁进行主观猜测。

最后，请按照以下JSON格式输出你的判断结果：
{
    "投诉倾向": "<是/否>",
    "原因": "<判断投诉倾向的原因>"
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
        prompt = original_prompt.replace("{{input}}", json.dumps(collection_dialog, ensure_ascii=False))

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
        target = filepath.replace("role", "complaint")
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
