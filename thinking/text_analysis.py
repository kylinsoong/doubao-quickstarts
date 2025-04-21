import os
from volcenginesdkarkruntime import Ark
import json
import time

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

if not API_KEY or not API_EP_ID:
    raise ValueError("Missing ARK_API_KEY or ARK_API_ENGPOINT_ID environment variables")

client = Ark(api_key=API_KEY)

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

def ask_ark(user_message: str):
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "user", "content": user_message}
        ],
        temperature=0.01
    )
    return completion.choices[0].message.content, completion.usage


@log_time
def main():
    with open('questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)    

    for idx, item in enumerate(data, 1):
        question = item['question']
        answer = item['answer']
        #print(question, answer)
        model_answer, usage = ask_ark(question)
        if answer.strip() == model_answer.strip():
            print("correct")
        else:
            print("expected: ", answer.strip(), "model answered: ", model_answer.strip())


if __name__ == "__main__":
    main()
