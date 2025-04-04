import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)


def load_prompt(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().strip() 
    

query = "康复医疗行业的定义是什么"
prompt = load_prompt("prompt.txt")

messages =[
    {
        "role": "system",
        "content": prompt
    },
    {
        "role": "user",
        "content": query
    }
]

completion = client.chat.completions.create(
    model=API_EP_ID,
    messages=messages,
    temperature=0.7,
)

print(completion.choices[0].message.content)

print(completion.usage)
