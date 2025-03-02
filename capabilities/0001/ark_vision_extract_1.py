import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt = """
分析图片，提取名称，法人代表，经费来源，以JSON 格式输出：
{"name":"名称","agency":"法人代表","source":"经费来源"}
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
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/0001/20250228-150109.jpeg"}
                },
            ],
        }
    ],
    temperature=0.01
)
print(completion.choices[0].message.content)

