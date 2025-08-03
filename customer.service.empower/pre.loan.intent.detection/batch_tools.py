import os
import tos
import time
import logging
import json
import concurrent.futures
import threading
from tos import HttpMethodType
from logging.handlers import RotatingFileHandler 
from pydub import AudioSegment
import requests
import wave
import contextlib
import io
import sys
import uuid
from volcenginesdkarkruntime import Ark
import random

#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_logging():
    log_format = '%(asctime)s - %(levelname)s - Thread %(thread)d - %(message)s'
    formatter = logging.Formatter(log_format)
    
    logging.basicConfig(level=logging.INFO)
    root_logger = logging.getLogger()
    
    root_logger.handlers = []
    
    file_handler = RotatingFileHandler(
        'processing.log',          # 日志文件名
        maxBytes=10*1024*1024,     # 单个文件最大10MB
        backupCount=5,             # 最多保留5个备份文件
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

setup_logging()

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


def generate_presigned_url(ak, sk, endpoint, region, bucket_name, object_key):
    try:
        client = tos.TosClientV2(ak, sk, endpoint, region)
        pre_signed_url_output = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key)
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


def get_wav_duration(url):
    try:
        response = requests.get(url, stream=True, timeout=10)  # 增加超时设置
        response.raise_for_status()  # 检查HTTP请求状态
        
        with io.BytesIO(response.content) as wav_buffer:
            with contextlib.closing(wave.open(wav_buffer, 'rb')) as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
                return duration
                
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for URL {url}: {str(e)}")
    except wave.Error as e:
        logging.error(f"Invalid WAV file from URL {url}: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error processing {url}: {str(e)}")
    
    return 60

def get_wav_duration(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with io.BytesIO(response.content) as wav_buffer:
        with contextlib.closing(wave.open(wav_buffer, 'rb')) as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            return duration


SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
API_APP_KEY = os.getenv("ASR_API_APP_KEY")
API_ACCESS_KEY = os.getenv("ASR_API_ACCESS_KEY")
API_RESOURCE_ID = os.getenv("ASR_API_RESOURCE_ID", "volc.bigasr.auc") 
API_SEQUENCE = os.getenv("ASR_API_SEQUENCE", "-1")

def asr_process(object_key, target_filename):

    output_dir = "asr"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, target_filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        logging.info(f"目标文件 {filepath} 已存在且内容有效，跳过ASR处理")
        return filepath


    ak = os.getenv('TOS_ACCESS_KEY')
    sk = os.getenv('TOS_SECRET_KEY')
    endpoint = os.getenv('TOS_ENDPOINT')
    region = os.getenv('TOS_REGION')
    bucket_name = os.getenv('TOS_BUCKET')

    url = generate_presigned_url(ak, sk, endpoint, region, bucket_name, object_key)
    audio_length = get_wav_duration(url)
    sleep_time = int(int(audio_length)/3)
    if sleep_time <= 2:
        sleep_time = 2    

    
    if not all([API_APP_KEY, API_ACCESS_KEY]):
        logging.error("ASR API环境变量ASR_API_APP_KEY和ASR_API_ACCESS_KEY未设置")
        return None

    request_id = str(uuid.uuid4())
    unique_user_id = str(uuid.uuid4())

    payload = {
        "user": {
            "uid": unique_user_id
        },
        "audio": {
            "format": "wav",  # 适配batch_tools处理的WAV文件
            "url": url
        },
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_ddc": True,
            "enable_punc": True,
            "enable_speaker_info": False,
            "enable_channel_split": True
        }
    }

    submit_headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": API_APP_KEY,
        "X-Api-Access-Key": API_ACCESS_KEY,
        "X-Api-Resource-Id": API_RESOURCE_ID,
        "X-Api-Request-Id": request_id,
        "X-Api-Sequence": API_SEQUENCE,
    }

    try:
        submit_response = requests.post(SUBMIT_URL, headers=submit_headers, json=payload)
        if submit_response.status_code != 200:
            logging.error(f"任务提交失败，状态码: {submit_response.status_code}，响应: {submit_response.text}")
            return None
        
        time.sleep(sleep_time)
        logging.info(f"任务 {request_id} 等待 {sleep_time} 秒后开始查询结果")

    except Exception as e:
        logging.error(f"提交任务时发生错误: {str(e)}")
        return None

    query_headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": API_APP_KEY,
        "X-Api-Access-Key": API_ACCESS_KEY,
        "X-Api-Resource-Id": API_RESOURCE_ID,
        "X-Api-Request-Id": request_id,
    }

    try:
        query_response = requests.post(QUERY_URL, headers=query_headers, json={})
        if query_response.status_code != 200:
            logging.error(f"结果查询失败，状态码: {query_response.status_code}，响应: {query_response.text}")
            return None

        asr_result = query_response.json()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(asr_result, f, ensure_ascii=False, indent=2)
        
        return filepath

    except Exception as e:
        logging.error(f"查询或保存结果时发生错误: {str(e)}")
        return None


def asr_extract(target_filename):

    output_dir = "input"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, target_filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        logging.info(f"目标文件 {filepath} 已存在且内容有效，跳过 ASR EXTRACT 处理")
        return filepath
  
    asr_filepath = os.path.join("asr", target_filename)

    try:
        with open(asr_filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        result = data['result']
        results = []
        if 'utterances' in result:
            utterances = result['utterances']
            for item in utterances:
                start_time = round(item['start_time'] / 1000, 2)
                end_time = round(item['end_time'] / 1000, 2)
                interval = f"{start_time} - {end_time}"
                utterance = {
                    "role": f"speaker-{item['additions']['channel_id']}",
                    "time": interval,
                    "text": item['text']
                }
                results.append(utterance)

        with open(filepath, 'w') as file:
            json.dump(results, file, ensure_ascii=False, indent=2)
        return filepath
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查文件路径。")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 存在 JSON 解析错误，请检查文件格式。")
    return None


API_KEY = os.environ.get("ARK_API_KEY")

models = [os.environ.get("ARK_API_ENGPOINT_ID_1"), os.environ.get("ARK_API_ENGPOINT_ID_2"), os.environ.get("ARK_API_ENGPOINT_ID_3")]

original_prompt_role_assign = """
    你是一名语音质检管理员，需要处理提供的电话对话。你的任务是分析整体对话，为“speaker - x”分配“客户”、“坐席”或“语音提示”的角色，然后将原对话中的“speaker - x”替换为分配后的角色，最后输出替换后的JSON数组。

    以下是催收对话：
    <催收对话>
    {{COLLECTION_DIALOG}}
    </催收对话>

在分析角色时，可依据以下规则：

    1. 坐席：主动介绍产品，提及账单、询问贷款意愿、提供借款方式和减免政策等与贷款业务相关信息的一方通常为坐席；
    2. 客户：对贷款时间、意愿、方式等提出疑问，说明自身困难情况，或接收坐席建议进行APP上操作的一方通常为客户。
    3. 提示音：通常位于对话开头，例如“温馨提示，来电启用隐私保护信息”, "对话已开启隐私保护，请接听"，“提醒，请勿透露身份及银行信息” 等为提示音。

# 输出格式
只输出替换角色后的JSON数组，不做额外的输出或解释。
"""


def role_assign(target_filename):

    output_dir = "role"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, target_filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        logging.info(f"目标文件 {filepath} 已存在且内容有效，跳过 Role Assign 处理")
        return filepath

    input_filepath = os.path.join("input", target_filename)


    try:
        with open(input_filepath, 'r', encoding='utf-8') as file:
            collection_dialog = json.load(file)
        prompt = original_prompt_role_assign.replace("{{COLLECTION_DIALOG}}", json.dumps(collection_dialog, ensure_ascii=False))

    except FileNotFoundError:
        logging.error(f"错误: 文件 {filepath} 未找到。")
        return None, None
    except json.JSONDecodeError:
        logging.error(f"错误: 无法解析 {filepath} 中的JSON数据。")
        return None, None
    except Exception as e:
        logging.error(f"发生未知错误: {e}")
        return None, None

    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=random.choice(models),
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=16000
    )

    message = completion.choices[0].message.content
    usage = completion.usage
    if message and usage:
        try:
            json_obj = json.loads(message)
        except json.JSONDecodeError:
            json_obj = message
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(json_obj, file, ensure_ascii=False, indent=2)
        logging.info(f"文件 {input_filepath} 的使用情况: {usage}")

        return filepath


original_prompt_tag = """
# 任务背景
这是一个贷款意图分类任务，目的是通过分析客户与坐席之间的对话内容，判断客户对贷款产品的意愿程度，以便于后续的精准营销和客户管理。准确的意图分类有助于提高转化率和客户满意度。

# 角色定义
你是一位专业的对话意图分析师，擅长从客户与坐席的对话中准确识别客户的真实意愿。你需要仔细阅读对话内容，分析客户的语言表达、情感倾向和行为意图，并根据提供的标签定义进行精确分类。

# 任务描述
你的任务是为给定的录音对话打标签。请仔细阅读以下录音对话，并根据提供的六个标签定义进行评估。你需要判断客户对贷款产品的意愿程度，或识别特殊情况（如投诉倾向或非本人对话）。

以下是JSON 结构化的对话内容：
<对话>
{{input}}
</对话>

# 标签定义

六个标签及其定义如下：

## 高意愿	

能有效沟通（参考交互轮次大于或等于3轮）能正常介绍产品（如客户额度/费用/优惠券/活动/还款方式），客户表示愿意操作或未拒绝操作。
a.坐席正常完成介绍，客户无异议表示愿意操作或未拒绝；
b.坐席在介绍过程中，客户主动提出对产品或操作流程感兴趣；
c.坐席在介绍过程中，客户虽提出异议坐席处理后客户未拒绝操作；

注意：
1. 坐席和客户的一次对话算一个交互轮次
2. 以上三点，满足任意一项，或多项都为高意愿

## 中意愿
	
能有效沟通（参考交互轮次大于或等于3轮）能正常介绍产品（如客户额度/费用/优惠券/活动/还款方式）但客户表示需要考虑或存在敷衍式应答，以下两种场景属于中意愿。
a.坐席正常完成介绍或介绍过程中，客户表示"需要考虑"等场景（如"回头再说"/"需要的时候再看"）
b.坐席正常完成介绍或介绍过程中，客户全程无明显回应，仅表示"知道了/好的/嗯"

注意：
1. 坐席和客户的一次对话算一个交互轮次

## 低意愿	

客户表示当前不愿意操作借款，以下两种场景属于低意愿
a.坐席在完整介绍或介绍过程中，客户表示对产品（如额度/费用/还款/提额降息/操作流程等）有异议且最终不愿意借款或暂时不需要
b.坐席在完成介绍或介绍过程中，客户表示对产品有异议后直接挂机

注意：
1. 客户提出一次异议，异议处理后客户表示不需要属于a场景 
2. a 场景和 b 场景的区分：b 场景客户提出额度费用等问题后直接挂机
3. 以上两种场景都属于低意愿

## 无意愿	

单通录音中客户明确表示不需要借款或主动挂机：
a.单通录音中，客户明确表示不需要借款等场景大于或等于2次；
b.在坐席介绍过程中，客户无回应直接挂机；

注意：
1. 客户第一次提出异议时不需要，异议处理后依然不需要属于a场景 
2. 无意愿b场景与低意愿的b场景区分: 无意愿的b场景是在介绍过程中客户无任何表示直接挂机，低意愿的b场景是客户提出了一个异议再直接挂机

## 投诉倾向	

客户出现投诉倾向、或出现辱骂、不文明用语、不再致电等负向情绪

注意：
1. 如出现以上场景，即使出现了意愿度场景，不进行打标

## 其他
如果客户明确说明打错电话，非本人接听，或者整个对话只有语音提示，则为其他，反之不为其他。
a.非本人，客户明确表示出自己不是本人（打错了等）
b.语音留言场景，如下为典型的语音留言场景：
  - 转至语音留言，你尝试联系的用户无法接通，请在提示音后录制留言，录音完成后挂断即可"（这个话术是固定的）
  - "你好，请留言后挂机，我会马上转达/你好，小微电话助手接通中，请问有什么事吗 "/您好，我是机主的电话秘书，请问有什么需要我为您转达的吗？"这类语音助手"

注意：
1 如果是语音留言，需要判断整体对话，是有客户或坐席讲话，如果有则不能标记为其他。

# 标签优先级
当对话同时符合多个标签条件时，请按以下优先级处理：
1. 投诉倾向（最高优先级）：当客户表现出投诉倾向时，无论是否同时表现出其他意愿，都应标记为"投诉倾向"
2. 意愿度标签（高意愿/中意愿/低意愿/无意愿）：在排除以上两种情况后，根据客户表现出的意愿程度进行分类

# 关键术语定义
1. "有效沟通"：指坐席和客户之间的对话内容与借款产品相关，且双方能够理解对方表达的意思，信息传递清晰
2. "正常介绍产品"：指坐席完整介绍了产品的核心信息，包括额度、费用、还款方式等至少两个方面的内容
3. "交互轮次"：坐席说一段话，客户回应一段话，算作一个完整的交互轮次
4. "异议"：客户对产品的某些方面（如额度、费用、还款方式等）表示疑问、不满或不理解

# 边界情况处理
1. 交互轮次恰好为3轮：需评估对话内容的充分性，若产品介绍不完整或客户回应不明确，则不能简单依据轮次判定
2. 客户回应模糊：当客户回应既不是明确拒绝也不是明确接受时，应根据整体对话语气和内容倾向判断
3. 对话中断：若对话突然中断且无法判断原因，应基于已有对话内容判断意愿度
4. 录音质量问题：若部分对话内容因录音质量问题无法辨识，应基于可辨识部分进行判断，若关键内容无法辨识，则标注为"无法判断"


# 分析步骤
请按以下步骤分析对话：
1. 确认对话参与者身份（是否本人）
2. 检查是否为语音留言场景
3. 识别客户情绪（是否有投诉倾向）
4. 计算有效交互轮次
5. 分析坐席产品介绍的完整性
6. 评估客户的回应态度和内容
7. 根据以上分析确定最终标签

# 自我检查
在给出最终标签前，请检查：
1. 是否正确计算了交互轮次
2. 是否考虑了所有相关的标签定义和注意事项
3. 客户的回应是否有明确的意愿表达
4. 是否存在特殊情况或边界情况需要特别处理
5. 标记结果只允许是六种标签中之一：高意愿/中意愿/低意愿/无意愿/投诉倾向/其

# 限制:
- 仅依据提供的坐席与客户对话记录进行意愿标注，不涉及其他无关话题。
- 标注结果必须严格对应上述各类意愿标准，不得随意偏离。
- 标记结果只允许是六种标签中之一：高意愿/中意愿/低意愿/无意愿/投诉倾向/其他 
- 回答需简洁明了，以json格式输出标注结果。

# 输出格式
请以JSON格式输出标注结果，包含标签（tag）和理由（reason）两个字段：

{
  "tag": "<高意愿/中意愿/低意愿/无意愿/投诉倾向/其他>",
  "reason": "<解释对应标注的原因，包括关键判断依据和符合的具体场景>"
}
"""



def audio_tagging(target_filename):
    output_dir = "loan"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, target_filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        logging.info(f"目标文件 {filepath} 已存在且内容有效，跳过 Tagging 处理")
        return filepath 

    role_filepath = os.path.join("role", target_filename)    

    try:
        with open(role_filepath, 'r', encoding='utf-8') as file:
            collection_dialog = json.load(file)
        prompt = original_prompt_tag.replace("{{input}}", json.dumps(collection_dialog, ensure_ascii=False))
    except FileNotFoundError:
        logging.error(f"错误: 文件 {filepath} 未找到。")
        return None
    except json.JSONDecodeError:
        logging.error(f"错误: 无法解析 {filepath} 中的JSON数据。")
        return None
    except Exception as e:
        logging.error(f"文件处理未知错误 [{filepath}]: {e}")
        return None

    try:
        client = Ark(api_key=API_KEY)
        completion = client.chat.completions.create(
            model=random.choice(models),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=16000
        )
    except Exception as e:
        logging.error(f"API调用失败 [{filepath}]: {e}")
        return None

    try:
        message = completion.choices[0].message.content
        usage = completion.usage
        if not (message and usage):
            logging.warning(f"API返回空结果 [{filepath}]")
            return None

        try:
            json_obj = json.loads(message)
        except json.JSONDecodeError:
            json_obj = message

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(json_obj, file, ensure_ascii=False, indent=2)
        logging.info(f"处理完成 [{filepath}]，结果写入: {target}，使用情况: {usage}")
        return filepath
    except Exception as e:
        logging.error(f"结果处理失败 [{filepath}]: {e}")
        return None



def execute(object_key):

    logging.info(f"Thread {threading.current_thread().ident} - Processing {object_key}")

    filename = os.path.splitext(os.path.basename(object_key))[0]
    target_filename = f"{filename}.json"

    asr_resp = asr_process(object_key, target_filename)
    if asr_resp is not None:
        logging.info(f"ASR processing {object_key} successful, result saved to: {asr_resp}")

    ext_resp = asr_extract(target_filename)
    if ext_resp is not None:
        logging.info(f"ASR result extracting {object_key} successful, result saved to: {ext_resp}")

    rol_resp = role_assign(target_filename)
    if ext_resp is not None:
        logging.info(f"Role Assign {object_key} successful, result saved to: {rol_resp}")


    tag_resp = audio_tagging(target_filename)
    if tag_resp is not None:
        logging.info(f"Tagging {object_key} successful, result saved to: {tag_resp}")



    print(object_key)


def main():

    object_keys = load_object_keys()
    max_workers = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(execute, object_keys)

if __name__ == "__main__":
    main()
