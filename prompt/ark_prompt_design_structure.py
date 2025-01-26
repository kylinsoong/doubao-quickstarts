import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

TIP = "引导结构和组织要求"


prompt = """请撰写一篇500字的文章，讨论城市绿化对空气质量改善的影响。文章应包括以下方面的内容：
  1. 引言：介绍城市绿化和其重要性。
  2. 影响空气质量的机制：解释树木和公园如何减少空气中的污染物。
  3. 可行性措施：讨论在城市规划中推广城市绿化的方法和挑战。
  4. 数据和案例研究：提供相关数据和至少两个城市绿化成功案例，以支持你的论点。
  5. 结论：总结城市绿化对空气质量的积极影响
"""

def main():
    print("==>", TIP)
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
