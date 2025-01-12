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
                {"type": "text", "text": "提取图表中的数据，按照此格式输出: {\"标题\":\"\", \"年份\":\"\",\"数据\":{\"年龄段\":\"\",\"占比\":\"\"}}"},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/chart-pie.jpg"}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

