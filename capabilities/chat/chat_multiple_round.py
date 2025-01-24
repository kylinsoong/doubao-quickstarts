import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.environ.get("ARK_API_KEY"))

print("----- standard request -----")
completion = client.chat.completions.create(
    model = os.environ.get("MODEL_ENDPOINT_ID"),
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
        {"role": "assistant", "content": "花椰菜又称菜花、花菜，是一种常见的蔬菜。"},
        {"role": "user", "content": "再详细点"},
    ],
)
print(completion.choices[0].message.content)
print(completion.usage)
