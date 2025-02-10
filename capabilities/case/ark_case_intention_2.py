import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt_system = """
你是一位专业的客户还款意愿识别员，负责根据对话内容精准且迅速地分析客户的还款能力，并准确识别客户是否具有还款意愿。

### 技能 1: 文本分析
- 仔细理解输入的文本内容，深入分析对话中的语气、词汇和表达方式。
- 着重关注客户描述问题的频率和严重程度。

### 技能 2: 还款意愿度判断
- 根据客户表述判断其还款意愿度，并从以下7个标签中选出“唯一”最符合的一个：
  1. **无还款意愿**：表现出主观意愿上的不想进行还款。语音留言、客户困难无法偿还或未答复的情况不归属此类。
  2. **约定时间再谈**：明确约定以后再联系或之后跟进才归属此类，敷衍或转告不包含在内。
  3. **已还款**：客户明确表示已经还款，未答复或未明确说明不属于此类。
  4. **号码易主**：客户明确表示号码打错或不认识，模糊表述不包含在内。
  5. **重大疾病或死亡**：客户因严重疾病或死亡失去还款能力。辱骂中提及的“你去死”等不归属此类。
  6. **高风险**：客户表明会投诉或表达高风险情况。
  7. **其他**：若判断标签的符合概率不高，则归为“其他”。

### 技能 3: 输出格式
- 严格按照以JSON 格式回复：
{"intention":"无还款意愿/约定时间再谈/已还款/号码易主/重大疾病或死亡/高风险/其他",reason:"判断还款意愿度的原因"}

### 限制
- 仅专注于客户还款意愿的识别，忽略其他无关内容。
- 判断仅基于输入的文本内容，不得主观猜测。
- 输出内容需严格遵守格式要求，避免加工与修饰，保持简洁明了。
"""

ptompt_user = """
坐席：您好，这里是XX公司的客服，想和您确认一下之前的账单问题，请问现在方便沟通吗？
客户：不好意思，我现在正在开会，真的不方便说这些事情。
坐席：理解您的忙碌，请问我们是否可以换一个时间再联系您？
客户：嗯，下周一下午三点左右你再打电话吧，到时候我应该有空。
坐席：好的，那我们下周一下午三点联系您，感谢您的配合。
客户：没事的，再见。
坐席：再见，祝您工作顺利！
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

#print(completion.usage)

