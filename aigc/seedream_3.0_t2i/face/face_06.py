import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

prompt="""
人脸照片，正脸对刷脸镜头，女性，35 岁，职业厨师，座在圆桌上吃饭，圆桌暗黄色，上面有汉字""。
"""

response = client.images.generate(
    model=os.environ.get("ARK_API_ENGPOINT_ID"),
    prompt=prompt,
    size="720x1280",
    seed=-1,
    watermark=False,
    response_format="url"        
)
print(response.data[0].url)
