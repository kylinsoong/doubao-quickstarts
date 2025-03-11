import requests
import uuid
import os
import time
from urllib.parse import urlparse


SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

def extract_filename(url):
    path = urlparse(url).path
    clean_path = path.split("~")[0].split("?")[0]
    return os.path.basename(clean_path)


def submit_task(payload, sleep_time, app_id, access_token, request_id):

    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": app_id,
        "X-Api-Access-Key": access_token,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": request_id,
        "X-Api-Sequence": "-1",
    }

    response = requests.post(SUBMIT_URL, headers=headers, json=payload)

    if response.status_code == 200:
        time.sleep(sleep_time)
        return request_id
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return None


def query_task(request_id, app_id, access_token, enable_speaker_info, enable_channel_split):

    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": app_id,
        "X-Api-Access-Key": access_token,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": request_id,
    }

    while True:
        response = requests.post(QUERY_URL, headers=headers, json={})
        if response.status_code == 200:
            data = response.json()
            if enable_speaker_info:
                buffer = ""
                for item in data['result']['utterances']:
                    speaker = item['additions']['speaker']
                    content = item['text']
                    current_str = f"speaker {speaker}: {content}"
                    if buffer:
                        buffer += '\n' + current_str
                    else:
                        buffer = current_str
                return buffer   
            elif enable_channel_split:
                buffer = ""
                for item in data['result']['utterances']:
                    channel_id = item['additions']['channel_id']
                    content = item['text']
                    current_str = f"channel {channel_id}: {content}"
                    if buffer:
                        buffer += '\n' + current_str
                    else:
                        buffer = current_str
                return buffer
            else:
                return data['result']['text']
        else:
            print(f"HTTP Error: {response.status_code}")
            print(response.text)

def handler(url, sleep_time, app_id, access_token, enable_speaker_info, enable_channel_split):
    request_id = str(uuid.uuid4())
    filename = extract_filename(url)

    if filename.lower().endswith('.mp3'):
        audio_format = 'mp3'
    elif filename.lower().endswith('.wav'):
        audio_format = 'wav'
    else:
        raise ValueError(f"不支持的音频文件格式，URL: {url}")
    
    unique_user_id = str(uuid.uuid4())

    if enable_speaker_info and enable_channel_split:
        enable_channel_split = False

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
            "enable_speaker_info": enable_speaker_info,
            "enable_channel_split": enable_channel_split
        }
    }

    submit_task(payload, sleep_time, app_id, access_token, request_id)
    results = query_task(request_id, app_id, access_token, enable_speaker_info, enable_channel_split)

    print(results)

app_id = os.getenv("ASR_API_APP_KEY")
access_token = os.getenv("ASR_API_ACCESS_KEY")

print(app_id, access_token)
handler("https://pub-kylin.tos-cn-beijing.volces.com/audio/005.wav", 50, app_id, access_token, True, False)
