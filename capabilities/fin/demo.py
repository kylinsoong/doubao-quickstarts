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
        return completion.choices[0].message.content, completion.usage
    except Exception as e:
        return e

prompt = """
你的任务是分析一组图片，分析结果将用于贷款授信。你需要仔细观察图片，分析图片中人的性别、年龄、表情、背景、是否戴眼镜。


请从以下几个维度进行分析：
1. 性别：明确图片中人的性别，只能填写“男”或“女”。
2. 年龄：判断图片中人的年龄，以年龄段的形式表示，例如“30 - 35”“35 - 40”等。
3. 职业：判断照片中人职业, 如果在办公室，则为白领
4. 表情：描述图片中人的表情。
5. 背景：详细描述背景情况，尽可能判断可能的地点，如公司、工厂、室外等。同时，说明背景中是否有人，如果有人，描述其动作。如果没有人则不输出"未见其他人"等描述
6. 戴眼镜：判断图片中人是否戴眼镜，只能填写“是”或“否”。
7. 是否遮挡：判断图片中是脸部是否有遮挡

以JSON格式输出分析结果，格式如下：
[
{"性别":"<男/女>","年龄":"<年龄>","职业":"<职业>","表情":"<表情>","背景":"<背景>","戴眼镜":"<是/否>", "脸部遮挡": "<是/否>"},
// 更多的照片的分析
]
"""


images = [
"https://pub-kylin.tos-cn-beijing.volces.com/9863/01.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/9863/02.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/9863/03.jpeg",
"https://pub-kylin.tos-cn-beijing.volces.com/9036/a83be6913a944d0b9e87f90e9b951040.jpeg",
"https://pub-kylin.tos-cn-beijing.volces.com/9863/04.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/9863/05.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/9863/06.jpg",
"https://pub-kylin.tos-cn-beijing.volces.com/9036/276e1023a6c74203b5a8df99e0b94273.jpeg"
]

results = ark_vision_images(images, prompt, 0.01)

print(results[0])
print(results[1])
