import os
import base64
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

image_path = "make_things_happen.jpg"

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)
client = Ark(api_key=API_KEY)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages = [
        {
            "role": "user",  
            "content": [  
                {"type": "text", "text": "图片传递的情绪是什么?"},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  f"data:image/jpg;base64,{base64_image}"}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

