import os
import tos

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')
base_path = "original"

try:
    client = tos.TosClientV2(ak, sk, endpoint, region)

    next_continuation_token = ''

    out = client.list_objects_type2(bucket_name,delimiter="/", prefix=base_path, continuation_token=next_continuation_token)

    print(out.is_truncated)
    print(out.next_continuation_token)
    print(out.common_prefixes)
    print(out.contents)

    for prefix in out.common_prefixes:
        print(prefix.prefix)

    for content in out.contents:
        print(content)

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
