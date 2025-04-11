import os
import tos
from tos import HttpMethodType

def generate_presigned_url(ak, sk, endpoint, region, bucket_name, object_key):
    try:
        client = tos.TosClientV2(ak, sk, endpoint, region)
        pre_signed_url_output = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key)
        return pre_signed_url_output.signed_url
    except tos.exceptions.TosClientError as e:
        print(f'Fail with client error, message: {e.message}, cause: {e.cause}')
    except tos.exceptions.TosServerError as e:
        print(f'Fail with server error, code: {e.code}')
        print(f'Error with request id: {e.request_id}')
        print(f'Error with message: {e.message}')
        print(f'Error with http code: {e.status_code}')
        print(f'Error with ec: {e.ec}')
        print(f'Error with request url: {e.request_url}')
    except Exception as e:
        print(f'Fail with unknown error: {e}')
    return None


def generate_presigned_urls(ak, sk, endpoint, region, bucket_name, object_keys):
    urls = []
    for key in object_keys:
        url = generate_presigned_url(ak, sk, endpoint, region, bucket_name, key)
        if url:
            urls.append(url)
    return urls


if __name__ == "__main__":
    ak = os.getenv('TOS_ACCESS_KEY')
    sk = os.getenv('TOS_SECRET_KEY')
    endpoint = "tos-cn-beijing.volces.com"
    region = "cn-beijing"
    bucket_name = "sec-kylin"
    object_keys = ["img/01.jpg", "img/02.jpg", "img/03.jpeg", "img/04.jpg"]
    urls = generate_presigned_urls(ak, sk, endpoint, region, bucket_name, object_keys)

    print(urls)
