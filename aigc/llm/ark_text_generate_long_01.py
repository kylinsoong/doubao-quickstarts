import os
import time
from volcenginesdkarkruntime import Ark

prompt = """
请撰写一篇长篇故事，故事情节：“小江得了重病，通过轻松筹平台获取了帮助”

# 要求
1. 内容积极向上
2. 字数要求 2 万字左右
3. 文章结尾必须总结字数，示例：（全文：xxx字）
"""

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

@log_time
def ark_chat():
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

    output_dir = "results/long/01"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{MODEL_ID}.result")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)


if __name__ == "__main__":
    ark_chat()
    
