import requests
import json
import os  

api_token = os.getenv("COZE_API_TOKEN")
if not api_token:
    raise ValueError("请设置环境变量 COZE_API_TOKEN 以存储您的API令牌")

url = "https://api.coze.cn/v3/chat"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

data = {
    "bot_id": "7531696470618554419",
    "user_id": "123123***",
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": "早上好",
            "content_type": "text"
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    
    response.raise_for_status()
    
    result = response.json()
    print("请求成功，响应结果：")
    print(json.dumps(result, indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"请求发生错误：{e}")
except json.JSONDecodeError:
    print("响应内容不是有效的JSON格式")
    
