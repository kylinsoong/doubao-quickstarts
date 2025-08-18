import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    api_key=os.environ.get("ARK_API_KEY")
)


completion = client.chat.completions.create(
    model="bot-20250812141711-xb7bd",  
    messages=[
        {"role": "user", "content": "新能源汽车行业发展趋势"},
    ],
)
print(completion.choices[0].message.content)
#if hasattr(completion, "references"):
#    print(completion.references)


