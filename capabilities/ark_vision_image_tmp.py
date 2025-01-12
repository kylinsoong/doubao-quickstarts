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
                {"type": "text", "text": ""},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  ""}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

