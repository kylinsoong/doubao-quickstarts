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
你的任务是从一组图片中提取prompt。如果两张图片中的prompt相同，则只提取一次，最后以 [{"prompt": "" },{"prompt": "" }...]的格式输出结果。

首先，你会看到一组图片：
<picture_set>
{{PICTURE_SET}}
</picture_set>

以下是提取prompt的步骤：
1. 依次查看每张图片中的prompt。
2. 对于第一个prompt，直接记录下来，格式为{"prompt": "第一个prompt内容"}。
3. 当查看下一个prompt时，与之前已经记录的prompt进行比较，如果与已记录的prompt不同，则按照格式{"prompt": "新的prompt内容"}记录下来。
"""

temperature = 0.1

results = ark_vision_images(frames, prompt, temperature)
print(results)

prompt = """
分析视频是用何种 AI 技术或产品生成，并点评该技术或产品
"""

temperature = 0.3

results = ark_vision_images(frames, prompt, temperature)
print(results)

prompt = """
你的任务是分析一组视频分帧产生的数据，并形成一篇不超过300字的说明性文章。在撰写文章时，不要提及图片，而是从视频的角度进行阐述。
以下是视频分帧产生的数据：
<video_frames_data>
{{VIDEO_FRAMES_DATA}}
</video_frames_data>
下面是形成文章的步骤：
1. 首先要理解视频分帧数据所反映的视频内容的大致情节或者主题。
2. 确定视频中的关键元素，如主要人物、场景、事件等，但不要描述成图片的样子。
3. 根据这些关键元素组织语言，按照逻辑顺序撰写文章。
4. 要注意语言简洁明了，保持在300字以内。
请在<article>标签内写出你的文章。
"""

temperature = 0.3

results = ark_vision_images(frames, prompt, temperature)
print(results)

prompt = """
你的任务是根据一个视频的描述创作一篇抒情性的文章，这篇文章要传递积极向上、鼓舞他人的意向，并且字数不超过300字。
首先，请仔细阅读视频的描述：
<video_description>
{{VIDEO_DESCRIPTION}}
</video_description>
在创作文章时，请遵循以下要求：
1. 文章要充满抒情性，表达积极乐观的情感。
2. 不要提及图片相关内容，只从视频的角度进行创作。
3. 语句通顺，用词恰当，能够有效地传达鼓舞人心的力量。
请在<抒情文章>标签内写下你的文章。
"""

temperature = 0.7

results = ark_vision_images(frames, prompt, temperature)
print(results)
