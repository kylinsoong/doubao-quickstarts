import os
import tos
import json
import numpy as np
import base64
import uuid

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')
object_key = "original/331_1741769819/10375.jpg"

client = tos.TosClientV2(ak, sk, endpoint, region)

result = client.head_object(bucket_name, object_key)

print(result.meta, result.meta.items())


for key, value in result.meta.items():
    print('meta key', key)
    print('meta value', value)
print('content-disposition', result.content_disposition)
print('content-type', result.content_type)
