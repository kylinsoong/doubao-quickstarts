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
你好，是ACME售后服务吗？是的，这里是ACME公司的售后服务中心，请问有什么可以帮您？我买了你们的一款智能扫地机器人，刚用不到两个月就出了问题，吸力很弱。上次联系你们售后，他们的态度很差，我对此非常不满。非常抱歉听到您的不满，请您具体说明一下问题，我们会尽力为您解决。问题就是，我觉得这是质量问题，但你们售后一直推卸责任，说是正常磨损，这让我很生气。真的非常抱歉，您反馈的情况我们会高度重视，我可以先为您安排免费更换一台设备，同时向上级反馈这个问题，争取为您提供更好的服务。那什么时候能更换呢？我们可以在三天内完成更换，新的设备会直接寄到您指定的地址，并附上一封致歉信。希望您能接受我们的解决方案。好吧，这次我接受，但希望你们以后改善售后服务，我不想再经历这样的事情。一定会的，我们会加强服务质量管理，真的非常感谢您的理解与配合。行，那就这样吧，谢谢。好的，感谢您的来电，祝您生活愉快！再见。
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
