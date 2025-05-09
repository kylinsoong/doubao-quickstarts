import os
import time
from volcenginesdkarkruntime import Ark

chapters = ["运动有益，但“过度”不等于更好", "当身体在说“不”——过度运动的常见表现", "医学警示——过度运动可能引发的严重后果", "如何判断你是否“运动过度”？", "科学运动原则——远离伤害，持久受益"]

chapter_prompt = """
你是医学科普文章写作助手, 根据如下<input>标签内用户输入的问题生成文章的一个章节，要求章节字数为300字左右

<input>
{MMMM}
</input>
"""

all_prompt = """
你是医学科普文章写作助手, 根据如下<inputs>标签内各章节内容，生成一篇完整文章。

<inputs>
{MMMM}
</inputs>

## 要求
1. 对各「章节内容」不做任何删减，各章节前后可以少许增加内容，以使文章连贯
2. 根据章节内容，为文章增加一个开头和结尾
3. 根据章节内容，为文章生成一个标题
"""


API_KEY = os.environ.get("ARK_API_KEY")

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper


def generate_chapter(prompt):

    API_KEY = os.environ.get("ARK_API_KEY")
    MODEL_ID = os.environ.get("ARK_MODEL_ID")

    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=16000,
        temperature=0.8
    )

    return completion.choices[0].message.content


@log_time
def ark_chat():

    contents = []
    for title in chapters:
        prompt = chapter_prompt.replace("{MMMM}", title)
        print(prompt)
        content = generate_chapter(prompt)
        contents.append(content)

    prompt = all_prompt.replace("{MMMM}", "\n\n".join(contents))

    API_KEY = os.environ.get("ARK_API_KEY")
    MODEL_ID = os.environ.get("ARK_MODEL_ID")

    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=16000,
        temperature=0.8
    )

    output_dir = "results/chapter/03"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{MODEL_ID}.result")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)


if __name__ == "__main__":
    ark_chat()
    
