import os
import json
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")


try:
    with open("sample.json", 'r', encoding='utf-8') as file:
        data_list = json.load(file)
except FileNotFoundError:
    print(f"文件 {json_file_path} 未找到，请检查文件路径是否正确。")
except json.JSONDecodeError:
    print(f"文件 {json_file_path} 不是有效的 JSON 格式，请检查文件内容。")

for data in data_list:
    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "user", "content": data['prompt']}
        ],
        temperature=0.01
    )

    #print(data['prompt'])    
    print(data['id'], completion.choices[0].message.content, data['正确回答'])
    #print()
