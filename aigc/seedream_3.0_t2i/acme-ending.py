import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

prompt = """
黑色背景，只包括如下字体，且按行显示，"A Film Produced By:" 为粗体，在第一行
"A Film Produced By:"
"Doubao-thinking-vision-pro"
"Doubao-Seedream"
"Doubao-Seedance"
"奇美拉数字人"
"剪映专业版"  
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
