import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

list_result = client.content_generation.tasks.list(
    page_num=1,
    page_size=10,
    status="queued",  # 按状态筛选, e.g succeeded, failed, running, cancelled
    model=API_EP_ID, # 按 ep 筛选
    # task_ids=["test-id-1", "test-id-2"] # 按 task_id 筛选
)
print(list_result)

