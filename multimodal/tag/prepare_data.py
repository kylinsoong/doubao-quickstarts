import os
import tos
import json
import numpy as np
import base64

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')
prefix = "original"

items = []

try:
    client = tos.TosClientV2(ak, sk, endpoint, region)

    truncated = True
    continuation_token = ''

    while truncated:
        result = client.list_objects_type2(bucket_name, prefix=prefix, continuation_token=continuation_token)
        for item in result.contents:
            if item.key.lower().endswith('.mp4'):
                items.append(item)
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

resulsts = {}

try:
    for item in items:
        tags = client.get_object_tagging(bucket_name, item.key)
        processed_tag_value = None
        for tag in tags.tag_set:
            if tag.key == "processed":
                processed_tag_value = tag.value
                break

        if processed_tag_value is not None:
            print(item.key, "already processed")
        else:
            subfolfer = item.key.split('/')[-1].removesuffix('.mp4')
            object_stream = client.get_object(bucket=bucket_name, key=item.key, process="video/info")
            video_info = json.load(object_stream)
            duration = video_info['format']['duration']
            duration = int(float(duration) * 1000)
            values = np.linspace(0, duration, 11, endpoint=False)[1:]
            video_frames = []
            for value in values:
                style = "video/snapshot,t_" + str(int(value))
                save_object = prefix + "/" +  subfolfer + "/" + str(int(value)) + ".jpg"
                save_bucket = bucket_name
                client.get_object(
                    bucket=bucket_name,
                    key=item.key,
                    process=style,
                    save_bucket=base64.b64encode(save_bucket.encode("utf-8")).decode("utf-8"),
                    save_object=base64.b64encode(save_object.encode("utf-8")).decode("utf-8")
                )
                video_frames.append("https://" + save_bucket + "." + endpoint + "/" + save_object)

            tag1 = tos.models2.Tag('author', 'kylin')
            tag2 = tos.models2.Tag('processed', subfolfer)
            client.put_object_tagging(bucket_name, item.key, [tag1, tag2])
       
            resulsts[subfolfer] = video_frames

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


with open("data.json", "w", encoding="utf-8") as f:
    json.dump(resulsts, f, ensure_ascii=False)
