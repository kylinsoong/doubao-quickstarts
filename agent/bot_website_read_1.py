import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    api_key=os.environ.get("ARK_API_KEY")
)

completion = client.chat.completions.create(
    model=os.environ.get("ARK_API_BOT_ID"),  
    messages=[
        {"role": "user", "content": "https://mp.weixin.qq.com/s/pZaBWNZYaUbsHzrqjFao-w"},
    ],
)


print(completion.choices[0].message.content)
