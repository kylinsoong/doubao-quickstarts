import os
import time
from volcenginesdkarkruntime import Ark
import threading
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


prompt = """
请撰写一篇 1500 字的医学科普文章，内容关于乳腺癌，要求文章 markdump 结构化输出.
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

def ark_chat(id):
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

    output_dir = "md3"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{id}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)

@log_time
def main():
    with ThreadPoolExecutor(max_workers=25) as executor:  
        executor.map(ark_chat, range(200))


if __name__ == "__main__":
    main()
    
