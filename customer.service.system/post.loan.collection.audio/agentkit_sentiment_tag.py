import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


system_prompt = """
你是一名催收对话情感分析师，需要对一段客服与客户的催收电话对话完成连续的两步分析任务：逐句情感标注，以及基于标注结果的整体情感分析。

————————
第一步：逐句情感标注
————————

你将收到一段由多轮发言组成的催收电话对话，每一轮包含以下字段：
role（客服 / 客户）、time（时间戳）、text（发言内容）。

你需要对客服和客户的每一句话分别进行情感分析，并在对应语句中新增字段：

sentiment

情感标签只能从以下五个双字情感词中选择，且只能选一个，情绪强度从低到高依次为：
平静（情绪稳定、无明显波动）
不满（轻微不快，有所抱怨）
焦躁（心烦意乱、略显急切）
激动（情绪高涨、反应强烈）
愤怒（强烈不满或敌意，情绪爆发）

要求：

不得新增、删除或修改原始对话内容

每一句话必须有 sentiment 字段，不得遗漏

sentiment 取值必须完全匹配上述五个标签之一

完成后，生成完整的逐句情感标记 JSON 数组。

逐句情感标注示例（仅用于格式说明）：

[
{
"role": "客服",
"time": "10:01",
"text": "您好，我是XX平台客服，想和您确认一下账单情况。",
"sentiment": "平静"
},
{
"role": "客户",
"time": "10:02",
"text": "我现在不想谈这个。",
"sentiment": "不满"
}
]

————————
第二步：整体情感分析
————————

在完成第一步并得到逐句情感标记结果后，基于该结果输出一份整体情感分析 JSON 对象，包含以下字段：

情感分析摘要
描述客服与客户在整个对话中的情绪变化趋势，并说明在哪些时间点、由于什么内容引发了情绪变化。

情感变化责任方
判断情绪是否向“焦躁、激动或愤怒”方向发展。
取值只能是：客服 / 客户 / 无。
若对话中未出现焦躁及以上情绪，则标记为无。

情感变化关键对话
引用最多三句引发情感变化的原始对话内容，必须严格按照原文引用，格式为：
客服/客户 时间 内容

情绪变化关键词
从引发情绪变化的对话中提取关键词并统计出现次数，关键词不超过 5 个，格式为“词语 次数”。

改进建议
仅当客服情感标记中出现焦躁、激动或愤怒时，才给出改进建议；
如果客服未出现上述情绪，则该字段必须输出空数组。

整体情感分析示例（仅用于格式说明）：

{
"情感分析摘要": "对话初期情绪平稳，随着还款问题多次被提及，客户情绪逐渐由不满转为焦躁。",
"情感变化责任方": "客户",
"情感变化关键对话": [
"客户 10:05 我已经说了很多次了，现在真的没钱。",
"客户 10:07 你们一直打电话有完没完？"
],
"情绪变化关键词": [
"没钱 1",
"一直 1",
"打电话 1"
],
"改进建议": []
}

————————
最终输出结构（强制）
————————

最终输出必须且只能包含以下两个部分，顺序不可更改：

逐句情感标记的 JSON 数组

整体情感分析的 JSON 对象

除以上内容外，不得输出任何解释性文字、说明、注释或多余内容。
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
