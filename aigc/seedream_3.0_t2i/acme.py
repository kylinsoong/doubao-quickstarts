import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

prompt = """
"ACME 金服数智化转型之路"，"ACME 金服"是一家金融服务公司，海报中使用时尚体，影像效果
"""

response = client.images.generate(
    model=os.environ.get("ARK_API_ENGPOINT_ID"),
    prompt=prompt,
    size="1280x720",
    seed=-1,
    watermark=False,
    response_format="url"        
)
print(response.data[0].url)
