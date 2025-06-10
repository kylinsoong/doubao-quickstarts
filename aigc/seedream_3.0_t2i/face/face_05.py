import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

prompt="""
人脸照片，女性，30 岁，戴项链，做在沙发上。
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
