import os
import time
from volcenginesdkarkruntime import Ark

prompt = """
你的任务是根据用户的问题或要求，撰写一篇约1500字的医学科普文章，并以Markdown格式输出。
以下是用户的问题或要求：
<question_or_request>
{{QUESTION_OR_REQUEST}}
</question_or_request>
在撰写文章时，请遵循以下指南：
1. 语言表达清晰、简洁，避免使用过于专业或生僻的医学术语，若必须使用，需进行通俗易懂的解释。
2. 文章内容应科学、准确，基于可靠的医学知识和研究成果。
3. 文章结构合理，有明确的开头、主体和结尾。开头应引出主题，引起读者兴趣；主体部分详细阐述相关医学知识；结尾进行总结或给出建议。
4. 可以适当使用案例、数据或图表等元素来增强文章的可读性和说服力，但要确保其真实性和相关性。
5. 整体风格应具有科普性和教育性，能够让普通读者轻松理解文章内容。
请直接输出文章。
"""

question = """
职场人抽烟有害健康
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
    API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

    client = Ark(api_key=API_KEY)
    new_prompt = prompt.replace("{{QUESTION_OR_REQUEST}}", question)
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "user", "content": new_prompt}
        ],
        temperature=0.2
    )

    print(completion.choices[0].message.content)
  
    print(completion.usage)


if __name__ == "__main__":
    ark_chat()
    
