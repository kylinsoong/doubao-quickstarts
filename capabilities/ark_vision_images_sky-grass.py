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
                {"type": "text", "text": "分析这两张图的内容，分别生成标签，以以下格式输出: {\"title\":\"\",\"label\":\"\"}"},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/sky-grass.jpg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/sky-grass-horse.jpg"}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

