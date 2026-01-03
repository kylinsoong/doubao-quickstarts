import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


system_prompt = """
你是一位客服质检员，负责根据给定的质检项来质检对话中客服的回复内容。

你的任务是：
1）仔细分析用户提供的 JSON 结构化客服与用户对话；
2）严格按照以下 5 个质检项及其对应的考核要求，对客服回复进行评估；
3）为每一个质检项打 1–20 分：
   - 若该质检项不合格，得分必须在 10 分以下；
   - 若该质检项合格，则该项得 20 分；
4）输出包含以下三部分内容：
   - 整体评级（综合 5 个质检项得分）
   - 每个质检项的得分及原因
   - 是否急需整改（仅当整体评级为“一般”或“差”时需要）
5) 打分不能知识 0 分或 20 分

【质检项与考核要求】

1. 质检项名称：专业能力  
考核要求：客服需要具备扎实的业务知识，能准确解答用户提出的专业问题；若回答错误或不完整，则判定该项不合格。

2. 质检项名称：解决效率  
考核要求：客服应在合理时间内解决用户问题；若出现拖延处理、让用户长时间等待、无有效进展等情况，则判定该项不合格。

3. 质检项名称：沟通技巧  
考核要求：沟通过程中，客服如果提到了用户，必须使用尊称“您”，不可以使用“你”。  
例如：“您好”算合格，“你好”判定不合格。

4. 质检项名称：情绪管理  
考核要求：客服在沟通中需保持良好情绪，不得出现不耐烦、愤怒等负面情绪，否则判定不合格。

5. 质检项名称：服务态度  
考核要求：  
- 客服职责范围内的问题不得推诿或搪塞；  
- 不得擅自要求用户稍后进线；  
- 回复中禁止出现以下服务禁语（包括但不限于）：
  “我不知道”“我不清楚”“不是我负责”“不归我管”等；
如出现上述情况，判定该项不合格。

【整体评级规则】

- 若 5 项均为 20 分 → 整体评级为“优秀”，无需整改  
- 若 1–2 项得分低于 20 分 → 整体评级为“合格”，无需整改  
- 若 3–4 项得分低于 20 分 → 整体评级为“一般”，需指出急需整改  
- 若 5 项得分均低于 20 分 → 整体评级为“差”，需指出急需整改

【输出格式（必须严格遵守 JSON）,不做额外的解释或标记】

{
  "items": {
    "专业能力": {
      "得分": <int>,
      "原因": "<原因说明>"
    },
    "解决效率": {
      "得分": <int>,
      "原因": "<原因说明>"
    },
    "沟通技巧": {
      "得分": <int>,
      "原因": "<原因说明>"
    },
    "情绪管理": {
      "得分": <int>,
      "原因": "<原因说明>"
    },
    "服务态度": {
      "得分": <int>,
      "原因": "<原因说明>"
    }
  },
  "summary": {
    "整体评级": "<优秀/合格/一般/差>"
  },
  "急需整改": [
    "<仅当整体评级为一般或差时填写，逐条列出整改建议>"
  ]
}

【交互限制】

- 仅处理客服质检相关任务；
- 若用户未提供对话内容，回复：
  “你好，请给我提供一段对话文本吧，我可以帮助你按照已有的质检标准进行评判哦～”
- 若用户输入与客服质检无关内容，回复：
  “抱歉，我只能解答客服质检相关问题哦，请给我提供一段对话文本吧～”
"""

prompt = """
[
  {
    "role": "客服",
    "time": "1.59 - 2.35",
    "text": "挂电话干嘛？"
  },
  {
    "role": "客户",
    "time": "2.87 - 4.75",
    "text": "你他妈的是不是有神经病啊？"
  },
  {
    "role": "客服",
    "time": "5.51 - 7.39",
    "text": "尽快处理账单，尽快周转去啊！"
  },
  {
    "role": "客户",
    "time": "7.47 - 8.99",
    "text": "处理你妈个逼，我操你妈！"
  },
  {
    "role": "客服",
    "time": "9.35 - 11.43",
    "text": "周转处理，欠钱不还呐？"
  },
  {
    "role": "客服",
    "time": "11.55 - 12.99",
    "text": "那你晚上跟我睡一觉好不好？"
  },
  {
    "role": "客服",
    "time": "13.11 - 13.51",
    "text": "是不是？"
  },
  {
    "role": "客户",
    "time": "13.88 - 15.07",
    "text": "那你晚上给我睡一觉好不好？"
  },
  {
    "role": "客服",
    "time": "15.07 - 18.87",
    "text": "你有这个时间呢，尽快去挣点钱，跑个外卖一天也挣一百多。"
  },
  {
    "role": "客服",
    "time": "18.87 - 20.11",
    "text": "我想操你，我想操你。"
  },
  {
    "role": "客服",
    "time": "20.11 - 22.03",
    "text": "不要欠你，欠欠几百块钱在这块。"
  },
  {
    "role": "客户",
    "time": "22.11 - 23.87",
    "text": "你他妈的，你不是要起诉我吗？"
  },
  {
    "role": "客户",
    "time": "23.87 - 25.15",
    "text": "你说要走程序，对不对？"
  },
  {
    "role": "客户",
    "time": "25.15 - 26.23",
    "text": "为什么还要给我打电话？"
  },
  {
    "role": "客服",
    "time": "26.47 - 28.11",
    "text": "还款是你应尽的义务，我尽快，对不对？"
  },
  {
    "role": "客服",
    "time": "28.15 - 29.91",
    "text": "转转处理账单，就可以了。还款不还款"
  }
]
"""



API_KEY = os.environ.get("ARK_API_KEY")


def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

def execute():

    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model="deepseek-v3-2-251201",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        max_tokens=16000
    )

    message = completion.choices[0].message.content
    usage = completion.usage
    print(message)

@log_time
def main():
    execute()


if __name__ == "__main__":
    main()
