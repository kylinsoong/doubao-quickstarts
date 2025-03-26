import os
import base64
from PIL import Image
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

image_path = "card.png"

def image_format(image_path):
    with Image.open(image_path) as img:
        image_format = img.format.lower()
        if image_format not in ["jpeg", "png", "gif", "bmp", "tiff"]:
            raise ValueError(f"Unsupported image format: {image_format}")
    return image_format

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)
format = image_format(image_path)
client = Ark(api_key=API_KEY)
print(image_path, format)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages = [
        {
            "role": "user",  
            "content": [  
                {"type": "text", "text": "图片是什么"},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  f"data:image/{format};base64,{base64_image}"}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

