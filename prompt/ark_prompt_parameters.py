import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)


def generate(temperature):
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "为画面谱写简短文案"},
                    {
                        "type": "image_url",
                        "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/wechat-moment.jpg"}
                    },
                ],
            }
        ],
       temperature = temperature
    )
    print(completion.choices[0].message.content)
    print("--------------------------------")


generate(1)
generate(0.9)
generate(0.7)
generate(0.5)
generate(0.3)
generate(0.1)
generate(0.01)

