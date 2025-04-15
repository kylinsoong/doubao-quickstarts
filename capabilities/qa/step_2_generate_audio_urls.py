import os
import tos
import time
import logging
import json
from tos import HttpMethodType

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


def generate_presigned_urls(ak, sk, endpoint, region, bucket_name, object_keys):
    urls = []
    for key in object_keys:
        url = generate_presigned_url(ak, sk, endpoint, region, bucket_name, key)
        file_name = os.path.basename(key)
        item = {
            "audio": file_name,
            "url": url
        }
        urls.append(item)
    return urls

@log_time
def main():
    ak = os.getenv('TOS_ACCESS_KEY')
    sk = os.getenv('TOS_SECRET_KEY')
    endpoint = os.getenv('TOS_ENDPOINT')
    region = os.getenv('TOS_REGION')
    bucket_name = os.getenv('TOS_BUCKET')

    object_keys = []
    try:
        with open('object_keys.txt', 'r') as file:
            for line in file:
                object_keys.append(line.strip())
    except FileNotFoundError:
        logging.error("The object_keys.txt file was not found.")
        return
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        return

    urls = generate_presigned_urls(ak, sk, endpoint, region, bucket_name, object_keys)

    with open('object_urls.json', 'w') as f:
        json.dump(urls, f)

if __name__ == "__main__":
    main()
