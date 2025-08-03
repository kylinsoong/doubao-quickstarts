import os
import time
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper


def load_json(file_path):
    #print(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def form_file_path(id, folder):
    file_path = f"{folder}/{id}.json"
    return file_path

@log_time
def main(json_path):
    data = load_json(json_path)
    results = []
    for idx, item in enumerate(data, 1):
        id = item['id']
        item.pop("url", None)

        seed = form_file_path(id, "huankuan")
        item["seed"] = load_json(seed)

        asr = form_file_path(id, "role")
        item["asr"] = load_json(asr)
        results.append(item)


    try:
        output_path = "results_tag_asr.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"处理完成，结果已写入 {output_path}")
    except IOError as e:
        print(f"错误：写入文件 {output_path} 失败 - {e}")

if __name__ == "__main__":
    json_path = "object_urls.json"
    main(json_path)
