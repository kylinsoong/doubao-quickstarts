import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

id = "cgt-20250507200859-s9pgb"
get_result = client.content_generation.tasks.get(task_id=id)

print(get_result)
