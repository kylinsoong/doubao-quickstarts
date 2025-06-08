import os
import time  
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

if __name__ == "__main__":
    print("----- create request -----")
    create_result = client.content_generation.tasks.create(
        model=os.environ.get("ARK_API_ENGPOINT_ID"),
        content=[
            {
                # 文本提示词与参数组合
                "type": "text",
                "text": "电影结尾，增加闪烁效果  --resolution 720p  --dur 5 --camerafixed false"
            },
            {
                # 图片URL
                "type": "image_url",
                "image_url": {
                    "url": "https://pub-kylin.tos-cn-beijing.volces.com/acme/acme-end.jpeg" #请上传可以访问的图片URL
                }
            }
        ]
    )
    print(create_result)

    # 轮询查询部分
    print("----- pooling task status -----")
    task_id = create_result.id
    while True:
        get_result = client.content_generation.tasks.get(task_id=task_id)
        status = get_result.status
        if status == "succeeded":
            print("----- task succeeded -----")
            print(get_result)
            break
        elif status == "failed":
            print("----- task failed -----")
            print(f"Error: {get_result.error}")
            break
        else:
            print(f"Current status: {status}, Retrying after 10 seconds...")
            time.sleep(10)
