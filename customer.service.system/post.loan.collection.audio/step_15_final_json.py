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
    data = load_json(json_path)
    for idx, item in enumerate(data, 1):
        id = item['id']
        item.pop("url", None)
        item.pop("length", None)

        input = form_file_path(id, "input")
        item["inputs"] = load_json(input)

        role = form_file_path(id, "role")
        item["roles"] = load_json(role)

        results = form_file_path(id, "results")
        item["results"] = load_json(results)

        huankuan = form_file_path(id, "huankuan")
        item["huankuan"] = load_json(huankuan)

        complaint = form_file_path(id, "complaint")
        item["complaint"] = load_json(complaint)

        intent = form_file_path(id, "intent")
        item["intent"] = load_json(intent)

        sentiment = form_file_path(id, "sentiment")
        item["sentiments"] = load_json(sentiment)        

        sentiment_summary = form_file_path(id, "sentiment_summary")
        item["sentiment_summary"] = load_json(sentiment_summary)

        abnormal = form_file_path(id, "abnormal")
        item["abnormals"] = load_json(abnormal)
 
        form = form_file_path(id, "form")
        item["forms"] = load_json(form)

        figure = form_file_path(id, "figure")
        item["figure"] = load_json(figure)

        figure_input = form_file_path(id, "test_json")
        with open(figure_input, "w", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False))

        logging.info(f"Saved data to {figure_input}")

         

if __name__ == "__main__":
    json_path = "object_samples.json"
    main(json_path)
