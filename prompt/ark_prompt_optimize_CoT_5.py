import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

TIP = "给模型 “思考”时间"

prompt = """
你是一个计算器，请你将用户输入的数字分别加上2，减去3，乘以3，除以2后直接输出计算结果，以','作为分隔符进行返回。
你可以参考以下的计算过程来帮助解决，
###
对于输入：1，2，3，4，5
计算过程如下。
首先分别对输入1，2，3，4，5加上2，得到：3, 4, 5, 6, 7
然后将3，4，5，6，7分别减去3，得到：0, 1, 2, 3, 4
然后将0，1，2，3，4分别乘以3，得到：0, 3, 6, 9, 12
最后将0，3，6，9，12分别除以2，得到：0, 1.5, 3, 4.5, 6
答案是：0, 1.5, 3, 4.5, 6
###
输入：2，4，6，8，10
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
