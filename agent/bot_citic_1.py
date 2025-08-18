import os
from volcenginesdkarkruntime import Ark
from urllib.parse import urlparse, urlunparse


client = Ark(
    api_key = os.environ.get("ARK_API_KEY")
)

system_prompt = "内容需要再50 个字以内"
prompt = "新能源汽车行业发展趋势"

completion = client.bot_chat.completions.create(
    model="bot-20250812141711-xb7bd",
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": prompt},
    ],
)

print(prompt)
print()
print(completion.choices[0].message.content)
