import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

TIP = "让模型扮演一个角色"

prompt = """你是一名科学家，请你就关于“黑洞是如何形成的?”的主题写一篇200字以内的文章
"""

def main():
    client = Ark(api_key=API_KEY)
    print("==>", TIP)
    print("<PRIMPT>: ", prompt)
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
