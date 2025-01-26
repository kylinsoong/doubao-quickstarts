import os
import json
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

TIP = """
"""


system_prompt = """
"""

prompt = """
"""

system_message = {
    "role": "system",
    "content": system_prompt
}
user_message = {
    "role": "user",
    "content": prompt
}

messages = [system_message, user_message]

def main():
    print("==>", TIP)
    print("<PROMPT>: ", prompt)
    print("<RESPONSE>:")
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=messages
    )

    print(completion.choices[0].message.content)
    print(completion.usage)


if __name__ == "__main__":
    main()
