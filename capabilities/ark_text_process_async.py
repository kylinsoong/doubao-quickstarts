import os
import asyncio
from volcenginesdkarkruntime import AsyncArk

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = AsyncArk(api_key=API_KEY)

async def main() -> None:
    stream = await client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
            {"role": "user", "content": "常见的十字花科植物有哪些？"},
        ],
        stream=True
    )
    async for completion in stream:
        print(completion.choices[0].delta.content, end="")
    print()


asyncio.run(main())
