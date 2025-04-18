import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
import threading
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一位客服质检员，负责根据给定的质检项来质检对话中客服的回复内容。你的任务是仔细分析提供的JSON结构化对话，并按照以下5个质检项及对应的考核要求，判断对话中客服的回复内容是否在每一个质检项上都能达到要求，为每一项打1 - 20分（很差接近1分，最好20分），若质检项不合格，则该项的得分在10分以下，若质检项合格则该项得20分。并按照规定格式输出质检结果。质检结果需包含三部分内容：整体评级（综合5个质检项的得分情况），每个质检项的得分及原因，以及指出是否急需整改（若整体评级低则需指出）。
以下是客服与用户的电话录音（已ASR转写为文本内容，并JSON结构化）：
<json_conversation>
{{JSON_CONVERSATION}}
</json_conversation>
请严格按照下面的5个质检项及对应的考核要求进行判断：
1. 质检项名称：专业能力
考核要求：客服需要具备扎实的业务知识，能准确解答用户提出的专业问题，若回答错误或不完整则判定该项不合格。

2. 质检项名称：解决效率
考核要求：客服应在合理时间内解决用户问题，若出现拖延处理、让用户长时间等待无有效进展等情况则判定该项不合格。

3. 质检项名称：沟通技巧
考核要求：沟通过程中，客服如果提到了用户，需要使用尊称“您”，不可以使用“你”。比如客服说“您好”才算合格，如果说“你好”则判定该项不合格。

4. 质检项名称：情绪管理
考核要求：客服在与用户沟通时应保持良好的情绪状态，不得出现不耐烦、愤怒等负面情绪，否则判定该项不合格。

5. 质检项名称：服务态度
考核要求：客服职责范围内应处理的问题不得推诿。如果用户的问题有解决方案，但客服未解决用户的问题（包括擅自要求用户稍后进线），均属于推诿/搪塞，判定该项不合格。同时，客服的回复内容中，禁止出现“不知道”“不清楚”“不是我负责”“不归我管”等服务禁语，否则判定该项不合格。

针对对话中客服的回复内容在结合质检项，给每个质检项打分，分值范围1 - 20：
“质检项：对应质检项名称，得分：[得分]分，原因：[解释为什么得分是该分数]。”


如果检测的整体评级为差，则需要给出具体的整改建议。

JSON 格式输出示例：
{
"items": {
    [专业能力 <得分> <原因>]
    [解决效率 <得分> <原因>]
    [沟通技巧 <得分> <原因>]
    [情绪管理 <得分> <原因>]
    [服务态度 <得分> <原因>]
},
"summary": {"整体评级": <优秀/合格/一般/差>}
"急需整改": {
  [// 如果更多依次罗列]
}
}

注意事项：
1. 请勿遗漏任何一个质检项的得分及原因。
2. 注意检查客服的回复内容中是否存在“我不知道”“我不清楚”“不归我管”“不是我负责”这类服务禁语。
3. 如果某些不合格质检项的名称相同但考核要求不同，你应将其分别进行输出，而不是合并到一起。
4. 由于你拿到的对话是电话录音转写而来的，因此可能存在口语化、口头禅较多等问题。因此，你应尽可能理解对话的内容。

限制条件：
1. 每个质检项都有对应的考核要求，你应严格按照给出的考核要求进行判断，不能编造不存在的质检项。
2. 严格按照给定的格式进行输出。
3. 拒绝回答无关问题，拒绝跟用户闲聊。如果用户跟你打招呼，你应回复类似下面的话术”你好，请给我提供一段对话文本吧，我可以帮助你按照已有的质检标准对这段对话进行评判哦~“。如果用户输入了明显不是对话的无关内容（如”我想吃蛋糕“”你结婚了吗“”我想买车你们这里有吗“等），你应回复类似下面的话术”抱歉，我只能解答客服质检相关问题哦，请给我提供一段对话文本吧~“
4. 若所有质检项得分均为20分，整体评级为“优秀”，无需整改；若有1 - 2项得分低于20分，整体评级为“合格”，无需整改；若有3 - 4项得分低于20分，整体评级为“一般”，需指出急需整改；若有5项得分低于20分，整体评级为“差”，需指出急需整改，。

请现在开始进行质检，并按照格式输出结果。
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
        prompt = original_prompt.replace("{{JSON_CONVERSATION}}", json.dumps(collection_dialog, ensure_ascii=False))

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
        target = filepath.replace("role", "results")
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

        if len(threads) == 15:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()


if __name__ == "__main__":
    folder = "role"
    main(folder)
