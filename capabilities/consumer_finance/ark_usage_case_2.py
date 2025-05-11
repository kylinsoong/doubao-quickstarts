import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

def ark_vision_images(item, prompt, temperature):
    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]
    try:
        completion = client.chat.completions.create(
            model=API_EP_ID,
            messages=messages,
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return e

prompt = """
你的任务是分析一组图片，分析结果将用于消费金融授信提额。你需要仔细观察图片，图片中包括房产证和行驶证。
其中房产证提取如下信息：
* 房屋所有权人
* 共有情况
* 房屋坐落
* 登记时间
* 房屋性质
* 规划用户
* 房屋建筑面积

机动车行驶证提取如下信息：
* 证件号：
* 状态：正常/异常
* 累计积分：当年累计扣分，例如 0 分
* 准驾车型：例如 C1, C2, B1, B2等
* 驾驶证有效期止
* 审验有效期止
* 下一清分日期
* 下一体检日期
* 联系方式

以JSON格式输出分析结果
"""


images = [
"https://pub-kylin.tos-cn-beijing.volces.com/9863/00101.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/9863/002.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/9863/003.jpg"
]

results = ark_vision_images(images, prompt, 0.01)

print(results)
