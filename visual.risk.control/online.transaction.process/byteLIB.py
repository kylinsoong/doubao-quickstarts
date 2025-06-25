import tos
import requests
import json
from tos import HttpMethodType
from volcenginesdkarkruntime import Ark
import time
import random
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


def generate_prompt():
    genders = ["男性", "女性"]
    ages = list(range(25, 65))  # 25岁到75岁
    wearing_features = ["无特殊佩戴", "戴耳环", "戴项链", "戴耳机", "戴眼镜", "戴氧气面罩", "有插管"]
    wearing_features_restricted = ["无特殊佩戴", "戴耳环", "戴项链", "戴耳机", "戴眼镜"]
    
    profession_common = ["白领"] * 8 + ["蓝领"] * 4
    profession_rare = ["司机", "警察", "消防员", "外卖员", "厨师", "保安"]
    profession_features = profession_common + profession_rare

    background_common = ["办公室"] * 4 + ["家"] * 2
    background_rare = ["医院", "赌场", "夜店", "中介", "车内", "火山", "上下铺"]
    background_environments = background_common + background_rare
    background_rare_restricted = ["办公室", "家"]    


    basic_features_common = ["无特殊特征"] * 1
    basic_features_rare = ["光头", "有纹身", "光膀子", "染发"]
    basic_features = basic_features_common + basic_features_rare
    
    coercion_features_common = ["无胁迫"] * 1
    coercion_features_rare = ["被扒眼睛", "被刀胁迫"]
    coercion_features = coercion_features_common + coercion_features_rare
    
    attack_features_common = ["无特殊处理"] * 1
    attack_features_rare = ["戴面具", "照片", "屏幕翻拍", "头模", "3D面具"]
    attack_features = attack_features_common + attack_features_rare
    
    emotion_common = ["平静"] * 5
    emotion_rare = ["愤怒", "悲伤", "厌恶", "恐惧", "惊讶"]
    emotion_features = emotion_common + emotion_rare

    gender = random.choice(genders)
    age = random.choice(ages)
    wearing = random.choice(wearing_features)
    profession = random.choice(profession_features)
    background = random.choice(background_environments)
    coercion = random.choice(coercion_features)
    attack = random.choice(attack_features)
    basic = random.choice(basic_features)
    emotion = random.choice(emotion_features)

    if basic == "无特殊特征" or coercion == "无胁迫" or attack == "无特殊处理":
        basic = "无特殊特征"
        coercion = "无胁迫"
        attack = "无特殊处理"
        emotion = "平静"
        wearing = random.choice(wearing_features_restricted)
        background = random.choice(background_rare_restricted)
    else:
        wearing = random.choice(wearing_features)

    prompt = (f"一张真实感的{gender}人脸图片，{age}岁，表情{emotion}，{wearing}，{basic}，职业是{profession}，"
              f"背景环境是{background}，{coercion}，{attack}，超高分辨率，细节丰富")
    
    return prompt



class ByteVLM:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger(__name__)

    def analyze_image(self, prompt, image_url, thinking=None, temperature=0.7, max_tokens=16000):
        if not self.api_key or not self.model:
            raise ValueError("Missing API_KEY or MODEL environment variables")

        client = Ark(api_key=self.api_key)

        message_content = [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url":  image_url}
            },
        ]

        params = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": message_content
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

 
        if thinking is not None:
            if isinstance(thinking, bool):
                thinking = "enabled" if thinking else "disabled"
            params["thinking"] = {"type": thinking}


        completion = client.chat.completions.create(**params)

        return completion.choices[0].message.content, completion.usage
        



    def analyze_video(self, prompt, video_url, thinking=None, fps=1.0, temperature=0.7, max_tokens=16000):
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
            "temperature": temperature,
            "max_tokens": max_tokens
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

