import os
from volcenginesdkarkruntime import Ark
from urllib.parse import urlparse, urlunparse

def remove_url_parameters(url):
    parsed = urlparse(url)
    cleaned = parsed._replace(query="", fragment="")  # 去掉 ? 和 #
    return urlunparse(cleaned)

client = Ark(
    api_key = os.environ.get("ARK_API_KEY")
)

prompt = "过度运动可能有害健康"

completion = client.bot_chat.completions.create(
    model="bot-20250509171516-4lf6h",
    messages = [
        {"role": "user", "content": prompt},
    ],
)

print(prompt)
print()
print(completion.choices[0].message.content)
print()
for r in completion.references:
    #print(remove_url_parameters(r.url))
    print(r.url)
