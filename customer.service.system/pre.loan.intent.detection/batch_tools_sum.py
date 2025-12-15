import os
import time
import json
import logging
import concurrent.futures
import threading

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


def load_object_keys():
    #keys = "object_keys.txt"
    keys = "object_keys_slim.txt"
    object_keys = []
    try:
        with open(keys, 'r') as file:
            for line in file:
                object_key = line.strip()
                if object_key.endswith('.wav'):
                    object_keys.append(object_key)
    except FileNotFoundError:
        logging.error("The object_keys.txt file was not found.")
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")

    return object_keys


def load_json(file_path):
    #print(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def form_file_path(id, folder):
    file_path = f"{folder}/{id}.json"
    return file_path


def execute(object_key):
    filename = os.path.splitext(os.path.basename(object_key))[0]
    target_filename = f"{filename}.json"
 
    asrpath = os.path.join("role", target_filename)
    asr = load_json(asrpath)

    tagpath =  os.path.join("loan", target_filename)
    tag = load_json(tagpath)

    result = {
        "audio": object_key,
        "asr": asr,
        "tag": tag
    }

    sumpath = os.path.join("result", target_filename)
    os.makedirs(os.path.dirname(sumpath), exist_ok=True)  # ensure the folder exists
    with open(sumpath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


@log_time
def main():
    object_keys = load_object_keys()
    max_workers = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(execute, object_keys)



if __name__ == "__main__":
    main()
