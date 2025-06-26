import json
import os
import time
import logging
from pydub import AudioSegment

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



def get_wav_length(file_path):
    try:
        audio = AudioSegment.from_wav(file_path)
        return len(audio) / 1000  # 转换为秒
    except Exception as e:
        print(f"Error getting length of {file_path}: {e}")
        return None

def update_json_with_wav_length(source_path, json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            if "audio" in item:
                audio = item["audio"]
                wav_path = os.path.join(source_path, audio)
                length = get_wav_length(wav_path)
                if length is not None:
                    item["length"] = length

        with open('object_samples.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)

        print("JSON file updated successfully.")
    except Exception as e:
        print(f"Error updating JSON file: {e}")

@log_time
def main():
    source_path = os.getenv('SOURCE_PATH')
    json_file_path = 'object_urls.json'
    update_json_with_wav_length(source_path, json_file_path)


if __name__ == "__main__":
    main()
