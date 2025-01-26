import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

TIP = "给模型 “思考”时间"

prompt = """
让我们一步步思考。
计算购买三个物品的总费用，第一个物品价格是 10 元，第二个物品价格比第一个物品贵 20 元，第三个物品价格是第二个物品价格的一半，求三件物品的总费用？
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
