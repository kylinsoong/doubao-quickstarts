import os
import tos
import time
import logging

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
    base_path = os.getenv('TOS_BASE_PATH', "juzi")
    ak = os.getenv('TOS_ACCESS_KEY')
    sk = os.getenv('TOS_SECRET_KEY')
    endpoint = os.getenv('TOS_ENDPOINT')
    region = os.getenv('TOS_REGION')
    bucket_name = os.getenv('TOS_BUCKET')

    tos_client = tos.TosClientV2(ak, sk, endpoint, region)

    audio_files = [f for f in os.listdir(source_path) if f.endswith('.wav')]

    object_keys = []
    for audio_file in audio_files:
        object_key = os.path.join(base_path, audio_file)
        object_filename = os.path.join(source_path, audio_file)
        upload_tos(tos_client, bucket_name, object_key, object_filename)
        object_keys.append(object_key)
        logging.info("uploaded %s", object_filename)

    output_file = 'object_keys.txt'
    try:
        with open(output_file, 'w') as f:
            for key in object_keys:
                f.write(key + '\n')
        logging.info(f"Successfully wrote object keys to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write object keys to file: {e}")


if __name__ == "__main__":
    main()
    
