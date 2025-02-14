import os
import json
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")


try:
    with open("cleaned_data.json", 'r', encoding='utf-8') as file:
        data_list = json.load(file)
except FileNotFoundError:
    print(f"文件 {json_file_path} 未找到，请检查文件路径是否正确。")
except json.JSONDecodeError:
    print(f"文件 {json_file_path} 不是有效的 JSON 格式，请检查文件内容。")


prompt ="""
# 角色
你是一个文本分类器，专门用于对视频 ASR 产生的字幕文本对话进行分类打标签。

# 任务
请根据给定的视频字幕或对话内容，将其分类为以下三种类型之一：

## 采访类
* 对话中有一个人提问，另一个人回答，并且提问者主导了话题的展开。
* 对话内容通常较正式，围绕特定话题展开，类似访谈或宣传介绍。
* 示例：
  - 文本：你为什么建议急需用钱的人去六六七借条上查看额度？可以介绍一下它的优势吗？
  - 标签：采访类

## 情景剧
* 多人对话，互动自然，没有明显的主导者，语气更随意，类似朋友或同事间的闲聊。
* 可能包含日常讨论、购物体验、借款经历等，不像采访那样有明确的问答关系。
* 示例：
  - 文本：我刚申请到了六六七借条的额度，最快五分钟放款，还可以分二十四期还款，真的很方便！
  - 标签：情景剧

## 其他
* 不符合以上两种分类，通常是单方面的信息输出，例如广告宣传、产品介绍等。
* 示例：
  - 文本：六六七借条授信额度最高可达二十万，最长可分二十四期还款，新用户还有免息优惠，快来申请吧！
  - 标签：其他

# 要求
请根据字幕的对话结构、语气和内容特点，将其正确归类为 “采访类”、“情景剧” 或 “其他”，回答为三个类型之一，不做额外解释。
"""


for data in data_list:
    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": data['text']}
        ],
        temperature=0.01
    )

    print(data['id'], completion.choices[0].message.content, data['label'])
