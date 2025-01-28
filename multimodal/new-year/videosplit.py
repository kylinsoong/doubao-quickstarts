import uuid
import os
import json
import tos
import numpy as np
import base64
import re

ak = os.getenv('VE_AK')
sk = os.getenv('VE_SK')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')

tos_client = tos.TosClientV2(ak, sk, endpoint, region)

def video_object_process(object_key, splittag):
    try:
        tags = tos_client.get_object_tagging(bucket_name, object_key)
        processed_tag_value = None
        for tag in tags.tag_set:
            if tag.key == "processed":
                processed_tag_value = tag.value
                break
        if processed_tag_value is not None:
            is_truncated = True
            next_continuation_token = ''
            video_prefix = processed_tag_value + "/"
            video_frames = []
            while is_truncated:
                out = tos_client.list_objects_type2(bucket_name, delimiter="/", prefix=video_prefix, continuation_token=next_continuation_token)
                is_truncated = out.is_truncated
                next_continuation_token = out.next_continuation_token
                for content in out.contents:
                    full_path = "https://" + bucket_name + "." + endpoint + "/" + content.key
                    video_frames.append(full_path)
            frames = []
            frame_prefix = ""
            for frame in video_frames:
                match = re.search(r'_([\d]+)\.jpg', frame)
                if match:
                    extracted_number = match.group(1)
                    frame_prefix = frame[0:len(frame) - len(extracted_number) - 4]
                    frames.append(int(extracted_number))
            sorted_frames = sorted(frames)
            processed_video_frames = []
            for i in sorted_frames:
                processed_video_frames.append(frame_prefix + str(i) + ".jpg")

            return processed_video_frames
        else:
            tag1 = tos.models2.Tag('author', 'kylin')
            tag2 = tos.models2.Tag('processed', splittag)
            tos_client.put_object_tagging(bucket_name, object_key, [tag1, tag2])
            object_stream = tos_client.get_object(bucket=bucket_name, key=object_key, process="video/info")
            video_info = json.load(object_stream)
            duration = video_info['format']['duration']
            duration = int(float(duration) * 1000)
            values = np.linspace(0, duration, 16, endpoint=False)[1:]
            file_name_with_ext = os.path.basename(object_key)
            file_name = os.path.splitext(file_name_with_ext)[0]
            video_frames = []
            for value in values:
                style = "video/snapshot,t_" + str(int(value))
                save_object = splittag + "/" + file_name + "_" + str(int(value)) + ".jpg"
                save_bucket = bucket_name
                video_frames.append("https://" + save_bucket + "." + endpoint + "/" + save_object)
                tos_client.get_object(
                    bucket=bucket_name,
                    key=object_key,
                    process=style,
                    save_bucket=base64.b64encode(save_bucket.encode("utf-8")).decode("utf-8"),
                    save_object=base64.b64encode(save_object.encode("utf-8")).decode("utf-8")
                )
            return video_frames
            
    except tos.exceptions.TosClientError as e:
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
        return False
    except tos.exceptions.TosServerError as e:
        print('fail with server error, code: {}'.format(e.code))
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
        return False
    except Exception as e:
        print('fail with unknown error: {}'.format(e))
        return False


value = str(uuid.uuid4())
frames = video_object_process("ve_newyear.mp4", value)
print(frames)

file_name = "frames.ini"

if os.path.exists(file_name):
    os.remove(file_name)

with open(file_name, 'w', encoding='utf-8') as file:
    for frame in frames:
        file.write(str(frame) + '\n')

print(file_name)
