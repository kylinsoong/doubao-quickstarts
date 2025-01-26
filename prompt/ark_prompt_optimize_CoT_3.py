import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

TIP = "给模型 “思考”时间"

prompt = """
让我们一步步思考。
仓库进了一批香蕉，第一天卖了全部的三分之一多 10 千克，第二天卖了剩余的一半少 5 千克，还剩 40 千克。这批香蕉原来有多少千克？
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
