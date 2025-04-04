import os
from volcenginesdkarkruntime import Ark

client = Ark(
    api_key = os.environ.get("ARK_API_KEY"), 
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

# standard:
print("----- standard request -----")
completion = client.bot_chat.completions.create(
    model=os.environ.get("ARK_BOT_ID"), 
    messages = [
        {"role": "system", "content": "智能助手"},
        {"role": "user", "content": "资本市场支持政策以来保险板块趋势"},
    ],
)
print(completion.choices[0].message.content)
print(completion.references)
