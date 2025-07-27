import os
import requests

PAT = os.getenv("COZE_API_TOKEN")
CONV_ID = os.getenv("COZE_CONVERSATION_ID")
CHAT_ID = os.getenv("COZE_CHAT_ID")

assert PAT, "请设置环境变量 COZE_API_TOKEN（并确保包含 retrieveConversation 权限）"
assert CONV_ID, "请设置环境变量 COZE_CONVERSATION_ID"

url = "https://api.coze.cn/v3/chat/retrieve"
headers = {
    "Authorization": f"Bearer {PAT}"
}
params = {
    "conversation_id": CONV_ID,
    "chat_id": CHAT_ID
}

resp = requests.get(url, headers=headers, params=params, timeout=10)
resp.raise_for_status()
result = resp.json()

if result.get("code") != 0:
    raise RuntimeError(f"调用失败：code={result.get('code')}, msg={result.get('msg')}")

data = result.get("data", {})
detail = result.get("detail", {})

print(data)
print()
print(detail)

