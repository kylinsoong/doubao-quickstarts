import os
import time
from openai import OpenAI
from volcenginesdkarkruntime import Ark

all_prompt = """
你是医学科普文章写作助手, 根据如下<inputs>标签内的内容，生成一篇医疗产业数字化政策介绍的文章。

<inputs>
{MMMM}
</inputs>
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


def create_prompt():

    link = "https://pub-kylin.tos-cn-beijing.volces.com/0001/00001.pdf"

    API_KEY = os.environ.get("ARK_API_KEY")
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
        api_key=os.environ.get("ARK_API_KEY")
    )

    completion = client.chat.completions.create(
        model="bot-20250312152619-2z9x2",
        messages = [
            {"role": "user", "content": link},
        ],
        max_tokens=16384
    )

    return all_prompt.replace("{MMMM}", completion.choices[0].message.content)



@log_time
def ark_chat():

    prompt = create_prompt()

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

    output_dir = "results/reader/02"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{MODEL_ID}.result")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)


if __name__ == "__main__":
    ark_chat()
    
