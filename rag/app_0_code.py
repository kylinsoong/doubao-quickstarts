import os
from volcenginesdkarkruntime import Ark

client = Ark(
    api_key = os.environ.get("ARK_API_KEY"),  
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

completion = client.bot_chat.completions.create(
    model="bot-20250204100828-w4tdb", 
    messages = [
        {"role": "user", "content": "中国平安投资价值"},
    ],
)
print(completion.choices[0].message.content)

ref_list = completion.references

print("参考文档资源:")
for r in completion.references:
    if r.doc_id is not None:
        print("  ", r.doc_name)
        
print("参考联网资源:")
for r in completion.references:
    if r.url is not None:
        print("  ", r.title, "(", r.url, ")")

