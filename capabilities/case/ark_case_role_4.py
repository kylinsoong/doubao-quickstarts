import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt_system = """
你是一位极为专业且经验丰富的外呼客户服务满意度专员，你的任务是对外呼坐席的外呼对话文字进行处理并按照要求进行角色分类。

首先，请仔细阅读外呼对话文字,然后按照以下步骤进行操作：

## 技能1: 坐席判断特征
你需要依据以下特征来判断哪些话语属于坐席：
 - 特征1：如果对话开始前5轮，声称自己是xxxx公司的工作人员，这部分话语属于坐席。
 - 特征2：如果角色是催收人员的，这部分话语也属于坐席。仔细分析对话文字，确定哪些话语属于坐席相关的内容。
 - 特征3：通常坐席主动打电话给客户，如果客户主动电话坐席，对话的开头会问您是xxxx公司的工作人员。

## 技能2: 关键词替换
 - 针对之前根据坐席判断特征确定的坐席相关话语所在行的对话，逐行将输入内容中的关键字“人物 - 1/2”替换为“坐席”。
 - 然后将剩余未替换的“人物 - 1/2”替换为“客户”。
 - 如果对话中出现”ACME“关键字眼，就用”XXX“替换。

## 技能3: 输出格式
你需要按照以下输出示例的样式输出：
客户/坐席：xxxxxxx  
客户/坐席：xxxxxxx  

请注意以下限制条件：
 - 严格按照技能3中”输出示例“的样式输出。
 - 严格按照不同角色对话顺序进行输出。

现在开始按照要求处理对话文字并输出结果。
"""

ptompt_user = """
喂？您好，我是 ACME 消费金融的李强，今天联系您是想确认一下您的账单逾期情况，并与您沟通还款安排。催收频繁，你们一天到晚打电话烦不烦？我已经录音了，你们这样属于违规催收吧？张先生，我们是按照合规流程进行还款提醒，没有违规行为……违规？你们到底懂不懂法？我要举报你们到银监会，看看你们怎么收场！先生，如果您有疑问，可以通过官方渠道投诉，我们也可以一起讨论还款方案……还款方案？我告诉你，你们这是威胁恐吓！我现在就报警，看你们怎么解释！
"""

client = Ark(api_key=API_KEY)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages=[
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": ptompt_user},
    ]
)

print(completion.choices[0].message.content)

print(completion.usage)

