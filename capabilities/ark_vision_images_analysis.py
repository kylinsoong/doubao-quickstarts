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
                {"type": "text", "text": "买篮子中的水果要花多少钱？"},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/fruits-basket.png"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/fruits-price-list.png"}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

