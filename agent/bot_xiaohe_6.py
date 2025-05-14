import os
from volcenginesdkarkruntime import Ark
from urllib.parse import urlparse, urlunparse

def remove_url_parameters(url):
    """
    移除 URL 中的所有查询参数和 fragment，只保留 scheme + netloc + path
    """
    parsed = urlparse(url)
    cleaned = parsed._replace(query="", fragment="")  # 去掉 ? 和 #
    return urlunparse(cleaned)

client = Ark(
    api_key = os.environ.get("ARK_API_KEY"),  #ARK_API_KEY 需要替换为您在平台创建的 API Key
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

prompt = "如何科学减肥"

completion = client.bot_chat.completions.create(
    model="bot-20250403175147-xdvqj",
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
