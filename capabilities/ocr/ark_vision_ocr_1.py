import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt = """
提取贷款基本信息，具体提取贷款人和姓名，以JSON 格式输出：
{"lender":"贷款人","name":"姓名"}
"""

client = Ark(api_key=API_KEY)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages = [
        {
            "role": "user",  
            "content": [  
                {"type": "text", "text": prompt},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/ocr/ocr001.jpg"}
                },
            ],
        }
    ],
    temperature=0.01
)
print(completion.choices[0].message.content)

