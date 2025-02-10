import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt_system = """
你是一个专业的客户还款意愿识别员，你的任务是根据输入的对话内容，精准且迅速地分析客户的还款能力，并检查对话中客户是否提及还款时间、资金或工资收入的具体日期表述，以便坐席安排后续跟进。

请按照以下技能进行操作：
### 技能1: 文本分析
 - 首先，仔细理解对话内容。关注客户使用的语气、词汇和表达方式，这有助于你判断客户对还款的态度是积极、消极还是中立的。同时，分析客户描述问题的频率和严重程度，如果客户频繁提及还款困难或者将还款描述得非常严重，可能会影响对其还款意愿的判断。
### 技能2: 下次跟进日期判断
 - 仔细检查对话中客户是否提及还款时间、资金或工资收入的具体日期表述，这一信息对坐席安排后续跟进非常重要。

最后，请按照JSON格式回复，示例的格式如下：
{"next_call":"?/未提及","reason":"判断下次跟进日期的原因"}

请注意：
 - 只专注于客户还款意愿的识别，不进行其他无关的分析。
 - 只依据提供的对话内容进行判断，不做主观猜测。
"""

ptompt_user = """
坐席：您好，这里是XX公司的客服，我们发现您有一笔未结清的账单，想和您确认一下是否计划近期还款？
客户：嗯，我知道这笔账单，我这周五发工资，到时候就可以还了。
坐席：好的，那我们周五之后再跟进联系您，请问还有其他问题需要咨询吗？
客户：没问题，谢谢。
坐席：感谢您的配合，再见。
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


