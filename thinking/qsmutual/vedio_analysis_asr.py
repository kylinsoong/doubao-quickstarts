import time
import os
import requests
import json
from volcenginesdkarkruntime import Ark

base_url = 'https://openspeech.bytedance.com/api/v1/vc'

appid = os.getenv("X_API_APPID")
access_token = os.getenv("X_API_TOKEN")

language = 'zh-CN'

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
def ac_video_caption(video_file_url):
    response = requests.post(
                 '{base_url}/submit'.format(base_url=base_url),
                 params=dict(
                     appid=appid,
                     language=language,
                     use_itn='True',
                     use_capitalize='True',
                     max_lines=1,
                     words_per_line=15,
                 ),
                 json={
                    'url': video_file_url,
                 },
                 headers={
                    'content-type': 'application/json',
                    'Authorization': 'Bearer; {}'.format(access_token)
                 }
             )
    print('submit response = {}'.format(response.text))
    assert(response.status_code == 200)
    assert(response.json()['message'] == 'Success')

    job_id = response.json()['id']
    response = requests.get(
            '{base_url}/query'.format(base_url=base_url),
            params=dict(
                appid=appid,
                id=job_id,
            ),
            headers={
               'Authorization': 'Bearer; {}'.format(access_token)
            }
    )
    assert(response.status_code == 200)
    utterances = response.json()
    return utterances


@log_time
def main():
   
    file_url = "https://pub-kylin.tos-cn-beijing.volces.com/0004/003.mp4"
    result = ac_video_caption(file_url)
    results = []
    if 'utterances' in result:
        utterances = result['utterances']
        for item in utterances:
            start_time = round(item['start_time'] / 1000, 2)
            end_time = round(item['end_time'] / 1000, 2)
            utterance = {
                "start_time": start_time,
                "end_time": end_time,
                "text": item['text']
            }
            results.append(utterance)
                
    
    with open("asr.json", 'w') as file:
        json.dump(results, file, ensure_ascii=False)



if __name__ == '__main__':
    main()
