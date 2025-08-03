import os
import tos

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = "tos-cn-shanghai.volces.com"
region = "cn-shanghai"
bucket_name = "haier-poc"
prefix = "haier"

try:
    client = tos.TosClientV2(ak, sk, endpoint, region)

    truncated = True
    continuation_token = ''

    with open('object_keys.txt', 'w', encoding='utf-8') as f:
        while truncated:
            result = client.list_objects_type2(bucket_name, prefix=prefix, continuation_token=continuation_token)
            for item in result.contents:
                f.write(item.key + '\n')
            truncated = result.is_truncated
            continuation_token = result.next_continuation_token

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

