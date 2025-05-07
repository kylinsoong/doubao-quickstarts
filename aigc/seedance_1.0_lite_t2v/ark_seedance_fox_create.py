import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)
create_result = client.content_generation.tasks.create(
    model=API_EP_ID, 
    content=[
        {
            # 文本提示词与参数组合
            "type": "text",
            "text": "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头，狐狸友善地抱着，镜头缓缓拉出，女孩的头发被风吹动  --ratio 16:9 --resolution 720p  --dur 10 --camerafixed false"
        }
    ]
)
print(create_result)

get_result = client.content_generation.tasks.get(task_id=create_result.id)
print(get_result)
