import os
import requests

PAT = os.getenv("COZE_API_TOKEN")  
WORKFLOW_ID = "7530827789084753956"

assert PAT, "需要设置环境变量 COZE_API_TOKEN"
assert WORKFLOW_ID, "需要设置 COZE_WORKFLOW_ID"

url = "https://api.coze.cn/v1/workflow/run"
headers = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json",
}

payload = {
    "workflow_id": WORKFLOW_ID,
    "parameters": {
        "input": "this is input",
        "file":["https://pub-kylin.tos-cn-beijing.volces.com/chapter1.docx","https://pub-kylin.tos-cn-beijing.volces.com/chapter2.docx"],
        "case": {"id":10001,"name":"test"}
    },
    "is_async": False
}

response = requests.post(url, headers=headers, json=payload)
resp = response.json()

if resp.get("code") != 0:
    raise RuntimeError(f"API 错误：code={resp.get('code')}, msg={resp.get('msg')}")

print("data", resp.get("data"))
print("debug_url", resp.get("debug_url"))

