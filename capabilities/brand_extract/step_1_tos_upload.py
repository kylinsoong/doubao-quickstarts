import os
import tos
import time
import json
import logging
from tos import HttpMethodType

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

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


def get_type(filename):
    _, file_extension = os.path.splitext(filename)
    type = file_extension.lstrip('.') 
    return type

def generate_presigned_urls(ak, sk, endpoint, region, bucket_name, object_keys):
    urls = []
    for index, key in enumerate(object_keys, start=1):
        url = generate_presigned_url(ak, sk, endpoint, region, bucket_name, key)
        file_name = os.path.basename(key)
        type = get_type(file_name)
        item = {
            "id": f"{index:04d}",
            "audio": file_name,
            "type": type,
            "url": url
        }
        urls.append(item)
    return urls

def upload_tos(tos_client, bucket_name, object_key, object_filename):
    try:
        logging.info("%s %s", object_key, object_filename)
        result = tos_client.put_object_from_file(bucket_name, object_key, object_filename)
        logging.info('http status code:%s, request_id: %s, crc64: %s', result.status_code, result.request_id,result.hash_crc64_ecma)
    except tos.exceptions.TosClientError as e:
        logging.error('fail with client error, message:%s, cause: %s', e.message, e.cause)
    except tos.exceptions.TosServerError as e:
        logging.error('fail with server error, code: %s', e.code)
        logging.error('error with request id: %s', e.request_id)
        logging.error('error with message: %s', e.message)
        logging.error('error with http code: %s', e.status_code)
        logging.error('error with ec: %s', e.ec)
        logging.error('error with request url: %s', e.request_url)
    except Exception as e:
        logging.error('fail with unknown error: %s', e)

@log_time
def main():
    source_path = os.getenv('SOURCE_PATH')
    base_path = os.getenv('TOS_BASE_PATH', "lkl")
    ak = os.getenv('TOS_ACCESS_KEY')
    sk = os.getenv('TOS_SECRET_KEY')
    endpoint = os.getenv('TOS_ENDPOINT')
    region = os.getenv('TOS_REGION')
    bucket_name = os.getenv('TOS_BUCKET')

    tos_client = tos.TosClientV2(ak, sk, endpoint, region)

    img_files = [f for f in os.listdir(source_path) if f.endswith('.jpg')]

    object_keys = []
    for audio_file in img_files:
        object_key = os.path.join(base_path, audio_file)
        object_filename = os.path.join(source_path, audio_file)
        upload_tos(tos_client, bucket_name, object_key, object_filename)
        object_keys.append(object_key)
        logging.info("uploaded %s", object_filename)

    urls = generate_presigned_urls(ak, sk, endpoint, region, bucket_name, object_keys)

    with open('object_urls.json', 'w') as f:
        json.dump(urls, f)


if __name__ == "__main__":
    main()
    
