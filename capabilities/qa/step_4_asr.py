import os
import requests
import time
import uuid
import json
import logging
import threading

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
API_APP_KEY = os.getenv("ASR_API_APP_KEY")
API_ACCESS_KEY = os.getenv("ASR_API_ACCESS_KEY")
API_RESOURCE_ID = os.getenv("ASR_API_RESOURCE_ID", "volc.bigasr.auc") 
API_SEQUENCE = os.getenv("ASR_API_SEQUENCE", "-1") 

if not all([API_APP_KEY, API_ACCESS_KEY]):
    raise EnvironmentError("Environment variables ASR_API_APP_KEY and  ASR_API_ACCESS_KEY must be set.")

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper


def submit_task(payload, sleep_time):

    requestid = str(uuid.uuid4())

    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": API_APP_KEY,
        "X-Api-Access-Key": API_ACCESS_KEY,
        "X-Api-Resource-Id": API_RESOURCE_ID,
        "X-Api-Request-Id": requestid,
        "X-Api-Sequence": API_SEQUENCE,
    }

    response = requests.post(SUBMIT_URL, headers=headers, json=payload)

    if response.status_code == 200:
        time.sleep(sleep_time)
        return requestid
    else:
        logging.error(f"HTTP Error: {response.status_code}")
        logging.error(response.text)
        return None

def query_task(request_id):

    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": API_APP_KEY,
        "X-Api-Access-Key": API_ACCESS_KEY,
        "X-Api-Resource-Id": API_RESOURCE_ID,
        "X-Api-Request-Id": request_id,
    }

    while True:
        response = requests.post(QUERY_URL, headers=headers, json={})
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logging.error(f"HTTP Error: {response.status_code}")
            logging.error(response.text)
            return None


def execute(id, audio_format, url, sleep_time):

    unique_user_id = str(uuid.uuid4())
    
    payload = {
        "user": {
            "uid": unique_user_id
        },
        "audio": {
            "format": audio_format,
            "url": url
        },
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_ddc": True,
            "enable_punc": True,
            "enable_speaker_info": True
        }
    }

    request_id = submit_task(payload, sleep_time)

    if request_id:
        results = query_task(request_id)
        #print(results)
        filename = f"{id}.json"
        filepath = os.path.join(".asr", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)
        thread_id = threading.get_ident()
        logging.info(f"Thread {thread_id} added {filepath}")


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@log_time
def main(json_path, num):
    data = load_json(json_path)
    threads = []
    for idx, item in enumerate(data, 1):
        id = item['id']
        type = item['type']
        length = item['length']
        sleep_time = int(int(length)/3)
        url = item['url']
        thread = threading.Thread(target=execute, args=(id, type, url, sleep_time))
        threads.append(thread)
        thread.start()
        #execute(id, type, url, sleep_time)

        if len(threads) == num:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

if __name__ == "__main__":
    json_path = "object_samples.json"
    main(json_path, 10)
