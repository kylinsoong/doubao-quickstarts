import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

completion = client.chat.completions.create(
    model="ep-20250213121225-s7jtg",
    messages=[
        {"role": "system", "content": "你是智能投研助手"},
        {"role": "user", "content": "2025 年纸黄金投资趋势分析"},
    ],
)
print(completion.choices[0].message.content)


