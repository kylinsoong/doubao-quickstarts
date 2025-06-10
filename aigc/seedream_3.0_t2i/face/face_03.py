import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

prompt="""
人脸照片，男性，30 多岁，背景在字节跳动公司前台。

前台后Logo 显示为 "Bytedance", 背景为蓝色
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
