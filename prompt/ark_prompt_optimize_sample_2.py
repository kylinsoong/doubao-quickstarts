import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

TIP = "提供样例"

prompt = """
请帮我分辨用户输入文本的类别是正面评价还是负面评价，请直接输出:正面评价/负面评价。
用户输入:我上周去看了这部电影，简直浪费时间。情节枯燥无味，演员的表现也差强人意。我真的后悔看了。
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
