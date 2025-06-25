import os
import requests
import uuid
from byteLIB import generate_prompt
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

prompt= generate_prompt()

response = client.images.generate(
    model=os.environ.get("ARK_API_ENGPOINT_ID"),
    prompt=prompt,
    size="864x1152",
    seed=-1,
    watermark=False,
    response_format="url"
)
print(response.data[0].url)

download_dir = os.path.expanduser("/Users/bytedance/Downloads/face")
file_name = os.path.join(download_dir, f"{uuid.uuid4()}.jpeg")

try:
    image_response = requests.get(response.data[0].url)
    if image_response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(image_response.content)
        print(f"图片已成功保存到 {file_name}")
    else:
        print(f"下载图片失败，状态码: {image_response.status_code}")
except requests.RequestException as e:
    print(f"请求过程中出现错误: {e}")


