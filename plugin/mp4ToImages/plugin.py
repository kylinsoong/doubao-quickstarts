from runtime import Args
from typings.mp4ToImages.mp4ToImages import Input, Output
import os
import requests
import tos
import uuid
import json
import numpy as np
import base64

def handler(args: Args[Input])->Output:

    url = args.input.url
    images_num = args.input.images_num
    endpoint = args.input.endpoint
    region = args.input.region
    bucket_name = args.input.bucket_name
    base_path = args.input.base_path
    ak = args.input.ak
    sk = args.input.sk
    
    errorMessage = ""
    client = tos.TosClientV2(ak, sk, endpoint, region)

    file_name = url.rsplit("/", 1)[-1]
    object_key = os.path.join(base_path, file_name)
    
    try:
        content = requests.get(url)
        client.put_object(bucket_name, object_key, content=content)
        content.close()
    except Exception as e:
        errorMessage = 'error: {}'.format(e)
   
    target = f"https://{bucket_name}.{endpoint}/{object_key}"
   
    img_folder = str(uuid.uuid4())
    total_images_num = images_num + 1
    video_frames = []

    try:
        tag1 = tos.models2.Tag('author', 'kylin')
        tag2 = tos.models2.Tag('images', img_folder)
        client.put_object_tagging(bucket_name, object_key, [tag1, tag2])
        object_stream = client.get_object(bucket=bucket_name, key=object_key, process="video/info")
        video_info = json.load(object_stream)
        duration = video_info['format']['duration']
        duration = int(float(duration) * 1000)
        values = np.linspace(0, duration, total_images_num, endpoint=False)[1:]
        file_name_with_ext = os.path.basename(object_key)
        file_name = os.path.splitext(file_name_with_ext)[0]
        for value in values:
            style = "video/snapshot,t_" + str(int(value))
            save_object = f"{base_path}/{img_folder}/{file_name}_{int(value)}.jpg"
            save_bucket = bucket_name
            client.get_object(
                    bucket=bucket_name,
                    key=object_key,
                    process=style,
                    save_bucket=base64.b64encode(save_bucket.encode("utf-8")).decode("utf-8"),
                    save_object=base64.b64encode(save_object.encode("utf-8")).decode("utf-8")
                )
            sub_target = f"https://{bucket_name}.{endpoint}/{save_object}"
            video_frames.append(sub_target)
    except Exception as e:
        errorMessage = 'error: {}'.format(e)

    if len(errorMessage) > 0:
        return {"images": [], "mp4": "", "": errorMessage}
    else:
        return {"images": video_frames, "mp4": target, "error": errorMessage}
