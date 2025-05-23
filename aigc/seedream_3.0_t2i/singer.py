import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

response = client.images.generate(
    model=os.environ.get("ARK_API_ENGPOINT_ID"),
    prompt="女歌手，民谣范，高饱和度，高对比，正面，生命力摄影，背景户外音乐节舞台",
    size="720x1280",
    seed=-1,
    watermark=False,
    response_format="url"        
)
print(response.data[0].url)
