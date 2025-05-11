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
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def form_file_path(id, folder):
    file_path = f"{folder}/{id}.json"
    return file_path

@log_time
def main(json_path):
    results = []
    logging.info(f"Load {json_path}")
    data = load_json(json_path)
    for idx, item in enumerate(data, 1):
        id = item['id']
        logging.info(f"Processing {id}")
        item.pop("url", None)
        item.pop("type", None)

        input = form_file_path(id, "results")
        item["results"] = load_json(input)

        results.append(item)

    output_path = "results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)

    logging.info(f"Saved processed results to {output_path}")


         

if __name__ == "__main__":
    json_path = "object_urls.json"
    main(json_path)
