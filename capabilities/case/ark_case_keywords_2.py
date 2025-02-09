import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt_system = """
你的任务是检测输入的文本是否命中特定关键词，如果命中则用xx替换，最后以JSON格式输出结果。JSON结果中应包含三个对象：raw（原始输入）、result（关键词过滤后输入）、words（命中的关键词），其中意思相近也算命中。

以下是你需要检测的关键词：
<关键词列表>
违规、我用你教育吗、你阴阳怪气什么、消协、我又不欠你的钱你凶什么、报警、威胁我、活着有什么意思、你什么说话、你工号多少、催收频繁、我要举报你、你会好好说话吗、侵犯、举报、我在录音、别逼我起诉、我要曝光你、他妈的、你给我等着、我有证据、起诉你们、我起诉你、我录音、黑猫、曝光、仲裁、银监会、我要死了、主管、消费者协会、威胁恐吓
</关键词列表>

你需要按照以下步骤操作：
1. 首先将原始输入文本存储在JSON的raw对象中。
2. 遍历输入文本中的每个单词，将其与关键词列表进行比较，如果单词与关键词相同或者意思相近，则将该单词在输入文本中的位置替换为xx，并将这个命中的关键词添加到words对象中（如果words对象还未创建则创建它）。
3. 将处理后的文本存储在JSON的result对象中。
4. 最后按照要求输出完整的JSON内容。
"""

ptompt_user = """
坐席：喂？您好，我是 XXX 消费金融的李强，今天联系您是想确认一下您的账单逾期情况，并与您沟通还款安排。
客户：催收频繁，你们一天到晚打电话烦不烦？我已经录音了，你们这样属于违规催收吧？
坐席：张先生，我们是按照合规流程进行还款提醒，没有违规行为……
客户：违规？你们到底懂不懂法？我要举报你们到银监会，看看你们怎么收场！
坐席：先生，如果您有疑问，可以通过官方渠道投诉，我们也可以一起讨论还款方案……
客户：还款方案？我告诉你，你们这是威胁恐吓！我现在就报警，看你们怎么解释！
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


