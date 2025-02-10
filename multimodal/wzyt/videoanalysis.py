import os
from volcenginesdkarkruntime import Ark


API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

def load_frames():
    file_path = 'frames.ini'
    frame_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                     frame_list.append(line)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查文件路径是否正确。")

    return frame_list

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
        return None

frames = load_frames()

prompt = """
你将执行一个分析一组图片的任务，任务的结果是判断图片中是否有给卡车加油，结果有两种：正常加油和没有加油。并且需要按照特定的判断逻辑得出结论，最后以JSON格式输出
结果。

下面是判断逻辑：
1. 如果有1张及以上图片显示看到一个戴着安全帽、身穿工作服的人拿着类似加油管的物件，站在一辆车旁边，且车是禁止的，则正常加油,否则显示没有加油
2. 在得出结论后，需要简单总结得出该结论的原因, 且结论出不出现图片字样，例如”图片中显示“，则描述为”视频中显示“。

以JSON格式输出结果，格式为{"result":"正常加油/没有加油", "reason":"判断的原因"}。
"""

temperature = 0.1

results = ark_vision_images(frames, prompt, temperature)
print(results)

