import os
import requests
import json

url = "https://open.feedcoopapi.com/agent_api/agent/chat/completion"

# Read from environment variables
api_key = os.getenv("SEARCH_API_KEY")
bot_id = os.getenv("SEARCH_BOT_ID")

if not api_key or not bot_id:
    raise ValueError("Please export BOT_ID and API_KEY as environment variables.")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "bot_id": bot_id,
    "stream": False,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "大模型技术2026年趋势总结"
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print("Status Code:", response.status_code)
print("Response:", response.text)

