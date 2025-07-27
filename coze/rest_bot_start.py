import os
import requests

PAT = os.getenv("COZE_API_TOKEN")
BOT_ID = "7530826517405286446"

assert PAT, "请设置环境变量 COZE_PERSONAL_ACCESS_TOKEN"
assert BOT_ID, "请设置环境变量 COZE_BOT_ID"

url = "https://api.coze.cn/v3/chat"
headers = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json"
}

payload = {
    "bot_id": BOT_ID,
    "user_id": "123456",
    "additional_messages": [
        { "role": "user", "content_type":"text", "content": "https://pub-kylin.tos-cn-beijing.volces.com/chapter1.docx, https://pub-kylin.tos-cn-beijing.volces.com/chapter2.docx, \"case\": {\"id\":10001,\"name\":\"test\"}, 分析对应文档" }
    ]
}

resp = requests.post(url, json=payload, headers=headers, timeout=20)
resp.raise_for_status()
data = resp.json()

if data.get("code") != 0:
    raise RuntimeError(f"Coze 接口调用失败：code={data.get('code')}, msg={data.get('msg')}")

reply = data.get("data", {}).get("reply") or data.get("data")
print("机器人回复：", reply)

