import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

def read_id_infos():
    try:
        with open('id_infos_01.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("id_infos_01.json 文件未找到")
        return []
    except json.JSONDecodeError:
        print("id_infos_01.json 文件格式错误")
        return []

def analyze_image(image_path, api_key, api_ep_id):
    prompt = """
    分析图片，提取姓名、性别、民族、出生、住址、身份证号码，以 JSON 格式输出
    {"name":"姓名", "gender":"性别", "nation":"民族", "birth":"出生", "address":"住址", "id_num":"身份证号码"}
    """
    client = Ark(api_key=api_key)
    completion = client.chat.completions.create(
        model=api_ep_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_path}
                    },
                ],
            }
        ],
        temperature=0.01
    )
    return completion.choices[0].message.content

# 比较识别结果和原始值
def compare_results(image_path, original_info, result):
    try:
        result_dict = json.loads(result)
        fields = ["name", "gender", "nation", "birth", "address", "id_num"]
        for field in fields:
            original_value = original_info.get(field)
            recognized_value = result_dict.get(field)
            if original_value != recognized_value:
                print(f"{image_path}, {field} 识别结果不一致，原始值: {original_value}，识别值: {recognized_value}")
            #else:
                #print(f"{image_path}, {field} 识别结果一致，值为: {original_value}")
    except json.JSONDecodeError:
        print("识别结果不是有效的 JSON 格式")

def execute(info):
    image_path = info.get('image_path')
    if image_path:
        result = analyze_image(image_path, API_KEY, API_EP_ID)
        compare_results(image_path, info, result)

@log_time
def main():
    id_infos = read_id_infos()
    if not id_infos:
        return

    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(execute, id_infos)

if __name__ == "__main__":
    main()
