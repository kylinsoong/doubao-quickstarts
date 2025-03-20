import os
import requests
import time
import uuid
import argparse
import json
from urllib.parse import urlparse

SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

API_APP_KEY = os.getenv("ASR_API_APP_KEY")
API_ACCESS_KEY = os.getenv("ASR_API_ACCESS_KEY")
API_REQUEST_ID = str(uuid.uuid4())
API_RESOURCE_ID = os.getenv("ASR_API_RESOURCE_ID") 
API_SEQUENCE = os.getenv("ASR_API_SEQUENCE", "-1") 

if not all([API_APP_KEY, API_ACCESS_KEY, API_RESOURCE_ID]):
    raise EnvironmentError("Environment variables ASR_API_APP_KEY, ASR_API_ACCESS_KEY, and ASR_API_RESOURCE_ID must be set.")


def submit_task(payload, sleep_time):

    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": API_APP_KEY,
        "X-Api-Access-Key": API_ACCESS_KEY,
        "X-Api-Resource-Id": API_RESOURCE_ID,
        "X-Api-Request-Id": API_REQUEST_ID,
        "X-Api-Sequence": API_SEQUENCE,
    }

    response = requests.post(SUBMIT_URL, headers=headers, json=payload)

    if response.status_code == 200:
        time.sleep(sleep_time)
        return API_REQUEST_ID
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return None

def query_task(request_id, detail, enable_speaker_info, enable_channel_split):

    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": API_APP_KEY,
        "X-Api-Access-Key": API_ACCESS_KEY,
        "X-Api-Resource-Id": API_RESOURCE_ID,
        "X-Api-Request-Id": API_REQUEST_ID,
    }

    while True:
        response = requests.post(QUERY_URL, headers=headers, json={})
        if response.status_code == 200:
            data = response.json()
            #print(data)
            if detail:
                #print(json.dumps(data, indent=4, ensure_ascii=False))
                print()
                if enable_speaker_info:
                    for item in data['result']['utterances']:
                        speaker = item['additions']['speaker']
                        content = item['text']
                        print(f"speaker {speaker}: {content}")
                    print()
                if enable_channel_split:
                    for item in data['result']['utterances']:
                        channel_id = item['additions']['channel_id']
                        content = item['text']
                        print(f"channel {channel_id}: {content}")
                    print()
            text = data['result']['text']
            print(text)
            break
        else:
            print(f"HTTP Error: {response.status_code}")
            print(response.text)


def validate_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme in ['http', 'https'], result.netloc]):
            return url
        else:
            raise argparse.ArgumentTypeError(f"{url} 不是有效的 HTTP 或 HTTPS URL。")
    except ValueError:
        raise argparse.ArgumentTypeError(f"{url} 不是有效的 URL。")


if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description="Submit and query a task.")
    parser.add_argument(
        "-s", "--sleep_time", 
        type=int, 
        default=3, 
        help="Time (in seconds) to sleep between submitting and querying the task."
    )
    parser.add_argument(
        "-u", "--url", 
        type=validate_url, 
        required=True, 
        help="URL of the audio file to be processed."
    )
    parser.add_argument(
        "-d", "--detail",
        action="store_true",
        help="Output detailed json"
    )
    parser.add_argument(
        "--enable_itn",
        action="store_true",
        default=False,
        help="Enable Speaker Info"
    )
    parser.add_argument(
        "--enable_punc",
        action="store_true",
        default=False,
        help="Enable Speaker Info"
    )
    parser.add_argument(
        "--enable_ddc",
        action="store_true",
        default=False,
        help="Enable Speaker Info"
    )
    parser.add_argument(
        "--enable_speaker_info",
        action="store_true",
        default=False,  
        help="Enable Speaker Info"
    ) 
    parser.add_argument(
        "--enable_channel_split",
        action="store_true",
        default=False,  
        help="Enable Channel Split"
    )
    args = parser.parse_args()

    unique_user_id = str(uuid.uuid4())

    url = args.url
    if url.lower().endswith('.mp3'):
        audio_format = 'mp3'
    elif url.lower().endswith('.wav'):
        audio_format = 'wav'
    else:
        raise ValueError(f"不支持的音频文件格式，URL: {url}")

    payload = {
        "user": {
            "uid": unique_user_id
        },
        "audio": {
            "format": audio_format,
            "url": args.url
        },
        "request": {
            "model_name": "bigmodel",
            "enable_itn": args.enable_itn,
            "enable_ddc": args.enable_ddc,
            "enable_punc": args.enable_punc,
            "enable_speaker_info": args.enable_speaker_info,
            "enable_channel_split": args.enable_channel_split
        }
    }

    request_id = submit_task(payload, args.sleep_time)

    if request_id:
        query_task(request_id, args.detail, args.enable_speaker_info, args.enable_channel_split)
