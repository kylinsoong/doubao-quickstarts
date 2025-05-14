import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

response = client.images.generate(
    model=os.environ.get("ARK_API_ENGPOINT_ID"),
    prompt="一只大熊猫在跳舞",
    size="1024x1024",
    response_format="url"        
)
print(response.data[0].url)
