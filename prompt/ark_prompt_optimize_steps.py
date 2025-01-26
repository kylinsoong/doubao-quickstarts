import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

TIP = "指定完成任务需要的步骤"

prompt = """
请按照以下步骤写一个故事：
1 先设定故事背景和角色。
2 描述角色的目标和遇到的困难。
3 讲述角色如何克服困难并最终实现了目标。
4 最后以一个有趣的结局来结束故事。
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
