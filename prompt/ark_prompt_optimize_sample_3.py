import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

TIP = "提供样例"

prompt = """
请根据以下分类的方式，帮我分辨用户输入文本的类别是正面评价或是负面评价，请直接输出：正面评价/负面评价。

请参考如下样例：
示例1：
用户输入：我昨晚去了这家餐厅，他们的食物和服务都令人惊艳。我绝对会再次光顾。
输出：正面评价

示例2：
用户输入：这本书我看过，部分情节还行，但是整体情节拖沓，比较一般。
输出：负面评价

示例3：
用户输入：我昨天看了这部电影，我觉得还可以，但是有些部分也有点无聊。
输出：负面评价

示例4：
用户输入：我上周去看了这部电影，简直浪费时间。情节枯燥无味，演员的表现也不尽人意。我真的后悔看了。
输出：负面评价

请回答如下问题：
用户输入：我最近在这家餐厅用餐，还行，但也不是特别惊艳。
输出：
"""

def main():
    client = Ark(api_key=API_KEY)
    print("==>", TIP)
    print("<PROMPT>: ", prompt)
    print("<RESPONSE>: ")
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message.content)

    print(completion.usage)

if __name__ == "__main__":
    main()
