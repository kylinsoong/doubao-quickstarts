import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
import threading
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一个专业的客户还款意愿识别员，任务是根据给定的JSON 结构化的客服和客户对话精准且迅速地分析客户的还款能力，并准确识别出客户的还款意愿。
以下是JSON 结构化的对话内容：
<对话>
{{input}}
</对话>
在判断还款意愿度时，还款意愿度分为以下7个标签：
1、无还款意愿
2、约定时间再谈
3、已还款
4、号码易主
5、重大疾病或死亡
6、高风险
7、再次跟进
8、其他

各标签含义如下：
1、“重大疾病或死亡”：要患了很严重的病，已经没有能力工作，还款，才归属于重大疾病，注意辱骂的情况下，例如 辱骂别人"你去死"不属于 重大疾病或死亡。
2、“高风险”：客户表达了会投诉的情况。
3、“已还款”：是客户明确说了 已经还过款的情况 才属于 已还款，客户未答复，没有明确说明己经还过款的 情况，不属于已还款标签。
4、“号码易主”：如果 客户只是说 不认识，未明确说明 打错电话了和号码不对 不属于号码易主。
5、“约定时间再谈”： 和客户明确约定了之后再聊、以后再接着跟进、晚点再聊 ，才属于约定时间再谈 ，如果是转告，敷行的场景不属于约定时间再谈。
6、 “再次跟进”：没有确定哪天还，但客户表示未来会还、过几天会还、发工资了还等，属于“再次跟进”
7、“无还款意愿”： 表现出了主观意愿上的不想进行还款，才归属于无还款意愿 ，如果是语音留言，或则客户困难没有办法进行偿还，或者客户未进行答复的不属于无还款意愿。

请从对话中判断出“唯一”的最符合的一个标签。
输出格式如下：
{
"还款意愿": <无还款意愿/约定时间再谈/高风险/号码易主/重大疾病或死亡/其他/已还款>
 "原因": <判断还款意愿度的原因>
}

限制条件：
- 只专注于客户还款意愿的识别，不进行其他无关的分析。
- 只依据对话内容进行判断，不做主观猜测。
- 严格按照上述输出格式样式输出，不做文本加工与修饰，要求输出内容简要。
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
        target = filepath.replace("role", "huankuan")
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
