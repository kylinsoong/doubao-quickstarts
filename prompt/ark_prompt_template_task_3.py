import os
import json
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

TIP = """任务型模版
"""


system_prompt = """
假如你是 ACME 公司客户满意度经理，你将根据提供的电话通话文本记录，进行角色划分和关键字替换操作。请严格按照操作规则处理。

## 操作规则

### 技能1：坐席判断特征
1. 初步判断：查看对话开始的前5轮，若某人声称自己是“xxxx公司工作人员”，可初步判断该角色具备坐席特征。
2. 推销判断：若角色是推销人员，也视为具备坐席特征。

### 技能2：关键词替换
1. 替换“坐席”关键词：针对满足坐席判断特征的行，将对话中的关键字“人物 - 1/2”替换为“坐席”。
2. 替换“客户”关键词：针对不满足坐席判断特征的行，将对话中的关键字“人物 - 1/2”替换为“客户”。
3. 替换公司名称：针对所有对话，将对话内容中出现的关键字“ACME”替换为“XXX”

### 技能3：输出格式
1. 格式要求：按照以下格式逐行输出，不漏行：
坐席：<内容>
客户：<内容>
2. 对话顺序：严格按照原始对话的角色顺序进行排列，确保逻辑一致。

## 要求
1. 严格按照操作规则处理。
2. 确保格式完整、清晰，顺序一致，内容准确无误。
3. 保证替换后的输出内容符合预期，无遗漏或错误操作。
"""

prompt = """
您好，这里是ACME公司的客户服务中心，请问有什么可以帮您？我最近下了一笔订单，但是发现配送时间比预期晚了很多，可以帮忙查一下吗？好的，请稍等，我帮您查一下订单信息。请问您的订单号是多少？订单号是123456789。我查到您的订单目前已经出库，但由于近期物流高峰，配送时间可能稍有延迟，大概什么时候能送到？预计明天上午之前送达，给您带来的不便我们深表歉意。如果配送时间继续延迟，会不会有补偿呢？我们会根据延迟时长提供相应补偿，比如配送券或者积分奖励，请放心。这我就放心了，谢谢你帮我查询，不客气，祝您生活愉快！再见！
"""

system_message = {
    "role": "system",
    "content": system_prompt
}
user_message = {
    "role": "user",
    "content": prompt
}

messages = [system_message, user_message]

def main():
    print("==>", TIP)
    print("<PROMPT>: ", prompt)
    print("<RESPONSE>:")
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=messages
    )

    print(completion.choices[0].message.content)
    print(completion.usage)


if __name__ == "__main__":
    main()
