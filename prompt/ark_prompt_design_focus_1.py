import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")


print("==>", "提供更多 query 相关的细节，可以获得更准确的答案")

client = Ark(api_key=API_KEY)

completion = client.chat.completions.create(
    model=API_EP_ID,
    messages=[
        {"role": "user", "content": "编写一篇太空探索的文章"}
    ]
)

print(completion.choices[0].message.content)
print(completion.usage)

print()

completion = client.chat.completions.create(
    model=API_EP_ID,
    messages=[
        {"role": "user", "content": "为一群10-15岁的孩子编写一篇介绍太空探索历史的文章。"}
    ]
)

print(completion.choices[0].message.content)
print(completion.usage)
