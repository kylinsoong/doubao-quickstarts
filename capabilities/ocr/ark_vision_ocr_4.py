import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt = """
提取图片中的姓名和身份证号，如果姓名或身份证包括 *  等特殊字符，则保留原始字符。以JSON 形式输出结果：
{"name":"姓名","ID":"身份证号"}
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
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/ocr/ocr004.jpg"}
                },
            ],
        }
    ],
    temperature=0.01
)
print(completion.choices[0].message.content)

