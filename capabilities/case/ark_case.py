import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt_system = """
TODO
"""

ptompt_user = """
TODO
"""

client = Ark(api_key=API_KEY)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages=[
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": ptompt_user},
    ]
)

print(completion.choices[0].message.content)

print(completion.usage)

