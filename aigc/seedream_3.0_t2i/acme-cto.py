import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

prompt = """
男性，CIO，正脸，电影感
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
