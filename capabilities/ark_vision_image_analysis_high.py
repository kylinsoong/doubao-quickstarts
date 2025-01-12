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
                {"type": "text", "text": "将图片内容转化为一个说明书"},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/vevm-bolling-methods.png"},
                    "detail": "high"
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

