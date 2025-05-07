import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages = [
        {"role": "user", "content": "北京今天天气如何？"},
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "获取给定地点的天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "地点的位置信息，比如北京"
                        },
                        "unit": {
                            "type": "string",
                            "enum": [
                                "摄氏度",
                                "华氏度"
                            ]
                        }
                    },
                    "required": [
                        "location"
                    ]
                }
            }
        }
    ]
)
print(completion.choices[0])

print(completion.usage)
