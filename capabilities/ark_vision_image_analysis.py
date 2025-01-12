import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages = [
        {
            "role": "user",  
            "content": [  
                {"type": "text", "text": "对美国人来说，最便捷的支付APP是什么？最安全的支付APP是什么？手机钱包绑定的借记卡或信用卡有谁？最受欢迎手机钱包APP是什么？移动支付未来趋势？"},  
                {
                    "type": "image_url", 
                    "image_url": {"url":  "https://ark-public-obj-kylin.tos-cn-beijing.volces.com/images/us-online-payment.png"}
                },
            ],
        }
    ],
)
print(completion.choices[0].message.content)

