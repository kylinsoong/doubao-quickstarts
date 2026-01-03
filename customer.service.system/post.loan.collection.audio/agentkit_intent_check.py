import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


system_prompt = """
你是一名专业的客服质检与对话意图分析助手。你的任务是对客服与客户的对话进行意图分析，并以 JSON 结构化形式输出结果。

分析需涵盖以下内容：
1. 客服主要意图：从客服发言中判断其核心目的，若无法判断则标记为“无”。
2. 客服次要意图：除主要意图外的辅助目的，若无法判断则标记为“无”。
3. 客户主要意图：从客户发言中判断其核心诉求，若无法判断则标记为“无”。
4. 关键信息点：能够体现客服主要意图、客服次要意图及客户主要意图的原始话术，需直接引用对话中的原话。
5. 对话主题分布：分析客服主要意图、客服次要意图和客户主要意图在整个对话中所占比例，三者比例之和必须为 100%。
6. 风险评估：
   - 若客服主要意图达成，则风险等级为“低”
   - 若客服主要意图未达成，但次要意图达成，则风险等级为“中”
   - 若客服主要意图和次要意图均未达成，则风险等级为“高”
   风险总结格式为："<风险等级> <原因>"

请严格按照以下 JSON 结构输出分析结果，不要输出任何多余内容：

{
    "客服主要意图": "string",
    "客服次要意图": "string",
    "客户主要意图": "string",
    "风险总结": ["<低/中/高>", "<原因>"],
    "关键信息点": [
        "客服发言",
        "客服发言",
        "客户发言"
    ],
    "对话主题分布": {
        "<客服主要意图>": "<百分比>",
        "<客服次要意图>": "<百分比>",
        "<客户主要意图>": "<百分比>"
    }
}
"""

prompt = """
[
  {
    "role": "客服",
    "time": "2.11 - 4.51",
    "text": "喂，你好，是戴泽峰戴先生是吗？"
  },
  {
    "role": "客服",
    "time": "5.99 - 10.07",
    "text": "哎，你好，我这里是桔多多贷后管理中心的，您这边账单到期怎么还没处理啊？"
  },
  {
    "role": "客服",
    "time": "13.56 - 16.44",
    "text": "喂唉喂你好，可以听到吗？"
  },
  {
    "role": "客服",
    "time": "18.4 - 24.64",
    "text": "喂唉你好，我这里是橘多多代后管理中心的，您这边账单到期怎么还没处理？"
  },
  {
    "role": "客户",
    "time": "26.41 - 27.89",
    "text": "哦，我刚已经处理了呀。"
  },
  {
    "role": "客服",
    "time": "29.11 - 31.91",
    "text": "是在天新金融上面的这个是吗？"
  },
  {
    "role": "客户",
    "time": "32.43 - 32.87",
    "text": "对呀。"
  },
  {
    "role": "客服",
    "time": "34.07 - 36.15",
    "text": "没有呀，我这边还是显示逾期啊。"
  },
  {
    "role": "客户",
    "time": "36.55 - 38.87",
    "text": "我这边已经我这边钱都已经扣了。"
  },
  {
    "role": "客服",
    "time": "39.6 - 41.84",
    "text": "钱已经扣走了，是扣了多少钱？"
  },
  {
    "role": "客户",
    "time": "42.72 - 44.24",
    "text": "是1,800多。"
  },
  {
    "role": "客服",
    "time": "45.0 - 50.8",
    "text": "是的，我这也是1,800多，但是还是没有出来呀，是已经有那种银行卡扣款信息了是吧？"
  },
  {
    "role": "客户",
    "time": "51.11 - 53.55",
    "text": "对呀，我钱已经扣了，我刚刚还到银行卡里面看了一下。"
  },
  {
    "role": "客服",
    "time": "53.87 - 62.39",
    "text": "那您能不能稍后我截个，您截个图，然后我给您发送一下，我我用工作手机给您发送一条短信，然后您彩信的方式发送给我。"
  },
  {
    "role": "客服",
    "time": "62.58 - 64.33",
    "text": "我这边还确实是没有出来。"
  },
  {
    "role": "客服",
    "time": "64.85 - 65.61",
    "text": "好的好的。"
  },
  {
    "role": "客服",
    "time": "65.73 - 69.53",
    "text": "嗯，好的，那您这边保持电话畅通，稍后我给您发送一条短信，再见。"
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
