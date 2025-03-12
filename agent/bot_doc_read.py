import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    api_key=os.environ.get("ARK_API_KEY")
)

completion = client.chat.completions.create(
    model=os.environ.get("ARK_API_BOT_ID"),  
    messages=[
        #{"role": "system", "content": "内容概要"},
        {"role": "user", "content": "https://pub-kylin.tos-cn-beijing.volces.com/0003/sample.docx"},
    ],
)


print(completion.choices[0].message.content)
