import os
import time
from volcenginesdkarkruntime import Ark

prompt = """
请撰写一篇 1500 字的科普文章，讨论城市绿化对空气质量改善的影响。文章应包括以下方面的内容：
  1. 引言：介绍城市绿化和其重要性。
  2. 影响空气质量的机制：解释树木和公园如何减少空气中的污染物。
  3. 可行性措施：讨论在城市规划中推广城市绿化的方法和挑战。
  4. 数据和案例研究：提供相关数据和至少两个城市绿化成功案例，以支持你的论点。
  5. 结论：总结城市绿化对空气质量的积极影响
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

    output_dir = "results/03"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{MODEL_ID}.result")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)


if __name__ == "__main__":
    ark_chat()
    
