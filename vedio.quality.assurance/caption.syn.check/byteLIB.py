import tos
import requests
import json
from tos import HttpMethodType
from volcenginesdkarkruntime import Ark
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

base_url = 'https://openspeech.bytedance.com/api/v1/vc'
language = 'zh-CN'

def log_time(func):
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

def load_file_content(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

class ByteVLM:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger(__name__)

    def analyze_video(self, prompt, video_url, thinking=None, fps=1.0, temperature=0.7):
        if not self.api_key or not self.model:
            raise ValueError("Missing API_KEY or MODEL environment variables")

        client = Ark(api_key=self.api_key)

        # Build message content
        message_content = [
            {"type": "text", "text": prompt},
            {
                "type": "video_url",
                "video_url": {
                    "url": video_url,
                    "fps": fps,
                    "detail": "low"
                }
            },
        ]

        # Configure API parameters
        params = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": message_content
                }
            ],
            "temperature": temperature  # Add temperature parameter
        }

        if thinking is not None:
            if isinstance(thinking, bool):
                thinking = "enabled" if thinking else "disabled"
            params["thinking"] = {"type": thinking}

        completion = client.chat.completions.create(**params)
        return completion.choices[0].message.content, completion.usage

    def process(self, prompt, video_url, thinking=None, fps=1.0, temperature=0.7):
        summary, usage = self.analyze_video(
            prompt, 
            video_url, 
            thinking=thinking,
            fps=fps,
            temperature=temperature  # Pass temperature to analyze_video
        )
        self.logger.info(f"Token usage: {usage}")
        return summary


class ByteVideoASR:
    def __init__(self, appid, access_token):
        self.appid = appid
        self.access_token = access_token

    def ac_video_caption(self, video_file_url):
        response = requests.post(
            f'{base_url}/submit',
            params=dict(
                appid=self.appid,
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
                'Authorization': f'Bearer; {self.access_token}'
            }
        )

        assert(response.status_code == 200)
        assert(response.json()['message'] == 'Success')

        job_id = response.json()['id']
        response = requests.get(
            f'{base_url}/query',
            params=dict(
                appid=self.appid,
                id=job_id,
            ),
            headers={
                'Authorization': f'Bearer; {self.access_token}'
            }
        )
        assert(response.status_code == 200)
        utterances = response.json()
        return utterances

    def process(self, file_url):
        result = self.ac_video_caption(file_url)
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

        return json.dumps(results, ensure_ascii=False, indent=2) 


class ByteTOS:

    def __init__(self, ak: str, sk: str, endpoint: str, region: str, bucket: str):
        self.ak = ak
        self.sk = sk
        self.endpoint = endpoint
        self.region = region
        self.bucket = bucket

    def generate_signed_url(self, object_key):
        try:
            client = tos.TosClientV2(self.ak, self.sk, self.endpoint, self.region)
            pre_signed_url_output = client.pre_signed_url(HttpMethodType.Http_Method_Get, self.bucket, object_key)
            return pre_signed_url_output.signed_url
        except tos.exceptions.TosClientError as e:
            logging.error(f'Fail with client error, message: {e.message}, cause: {e.cause}')
        except tos.exceptions.TosServerError as e:
            logging.error(f'Fail with server error, code: {e.code}')
            logging.error(f'Error with request id: {e.request_id}')
            logging.error(f'Error with message: {e.message}')
            logging.error(f'Error with http code: {e.status_code}')
            logging.error(f'Error with ec: {e.ec}')
            logging.error(f'Error with request url: {e.request_url}')
        except Exception as e:
            logging.error(f'Fail with unknown error: {e}')
        return None

    def generate_signed_urls(self, object_keys):
        return [self.generate_signed_url(key) for key in object_keys]

