import os
import tos
import time

base_path = os.getenv('TOS_BASE_PATH', "/path/to/mp4/")
ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')

tos_client = tos.TosClientV2(ak, sk, endpoint, region)

def upload_tos(object_key, object_filename):
    try:
        result = tos_client.put_object_from_file(bucket_name, object_key, object_filename)
        print('http status code:{}'.format(result.status_code), 'request_id: {}'.format(result.request_id), 'crc64: {}'.format(result.hash_crc64_ecma))
    except tos.exceptions.TosClientError as e:
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
    except tos.exceptions.TosServerError as e:
        print('fail with server error, code: {}'.format(e.code))
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
    except Exception as e:
        print('fail with unknown error: {}'.format(e))


video_files = [f for f in os.listdir(base_path) if f.endswith('.mp4')]

for video_file in video_files:
    object_key = video_file
    object_filename = os.path.join(base_path, video_file)
    upload_tos(object_key, object_filename)
    print(f"uploaded {object_filename}")
    time.sleep(5) 

