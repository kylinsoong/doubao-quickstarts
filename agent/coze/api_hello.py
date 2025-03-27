import os
import requests

url = 'https://api.coze.cn/v3/chat'
# 从环境变量中读取授权令牌
auth_token = os.getenv('COZE_API_TOKEN')
bot_id = os.getenv('COZE_BOT_ID')
if not auth_token:
    raise ValueError("环境变量 COZE_API_TOKEN 未设置。")

headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
}
data = {
    "bot_id": bot_id,
    "user_id": "121451",
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": "https://pub-kylin.tos-cn-beijing.volces.com/citic/report_20250304_142139.docx",
            "content_type": "text"
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print(response.json())
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP 错误发生: {http_err}')
except Exception as err:
    print(f'其他错误发生: {err}')
    
