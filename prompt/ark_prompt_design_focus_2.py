import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

TIP = "提供更多 query 相关的细节，可以获得更准确的答案"

def main():
    print("==>", TIP)
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "user", "content": "请写一篇文章，关于环保的，500字"}
        ]
    )

    print(completion.choices[0].message.content)

    print(completion.usage)

    print()

    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "user", "content": "请撰写一篇500字的文章，讨论城市绿化对空气质量改善的影响。文章应包括以下方面的内容：城市绿化的定义，如树木和公园的增加，它们如何减少空气中的污染物，以及在城市规划中推广城市绿化的可行性措施。请提供相关数据和案例研究以支持你的论点。"}
        ]
    )

    print(completion.choices[0].message.content)

    print(completion.usage)

if __name__ == "__main__":
    main()
