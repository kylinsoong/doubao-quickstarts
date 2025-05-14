import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

response = client.images.generate(
    model=os.environ.get("ARK_API_ENGPOINT_ID"),
    prompt="人物：东方古典鹅蛋脸，简约高发髻佩戴发饰, 眼神中充满力量, 背景有荷花、祥云元素，具有力量感与艺术感",
    size="1024x1024",
    response_format="url"        
)
print(response.data[0].url)
