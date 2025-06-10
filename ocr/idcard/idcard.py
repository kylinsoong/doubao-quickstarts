import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt = """
分析图片，提取姓名、性别、民族、出生、住址、身份证号码、签发机关、有效期，以 JSON 格式输出
{"name":"姓名", "gender":"性别", "nation":"民族", "birth":"出生", "address":"住址", "id_num":"身份证号码", "issue":"签发机关", "valid":"有效期"}
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
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/8769/idcard-a.jpeg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url":  "https://pub-kylin.tos-cn-beijing.volces.com/8769/idcard-b.jpeg"}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

