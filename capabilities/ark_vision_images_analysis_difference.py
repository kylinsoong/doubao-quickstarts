import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages = [
        {
            "role": "user",  
            "content": [  
                {"type": "text", "text": "图 1 显示的是什么？在什么地方？两幅图有什么相似处，两幅图有什么不同？"},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/Feldherrnhalle-1.jpeg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/Feldherrnhalle-2.jpeg"}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

