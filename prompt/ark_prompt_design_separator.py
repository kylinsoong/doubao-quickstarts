import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

print("==>", "使用分隔符去更清晰地区分输入的不同部分")

text1 = '''火山方舟是火山引擎推出的大模型服务平台，提供模型训练、推理、评测、精调等全方位功能与服务，并重点支撑大模型生态。 火山方舟通过稳定可靠的安全互信方案，保障模型提供方的模型安全与模型使用者的信息安全，加速大模型能力渗透到千行百业，助力模型提供方和使用者实现商业新增长。'''
text2 = '''常见的十字花科植物有白菜、萝卜、西兰花、花椰菜等，它们都属于十字花科，是人们餐桌上常见的蔬菜，富含多种维生素和营养物质。'''

prompt = f"请把以下用三个引号括起来的文本分别总结成一句话：\n'''{text1}'''\n'''{text2}'''"

client = Ark(api_key=API_KEY)

completion = client.chat.completions.create(
    model=API_EP_ID,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(completion.choices[0].message.content)

print(completion.usage)
