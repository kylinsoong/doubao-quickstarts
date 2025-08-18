import os
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time
from byteLIB import generate_urls
from byteLIB import compute_real_bbox
import json

def initialize_clients():


    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")

    vlm = ByteVLM(api_key=api_key, model=model)

    return vlm


def generate_prompt():
    prompt = load_file_content("prompt.object.detect.complex.ini")
    return prompt

def process_videos(vlm, url):
    prompt = generate_prompt()
    results = vlm.process(prompt=prompt, video_url=url, thinking="enabled", max_tokens=32000)
    print(results)
    objs = json.loads(results)
    for obj in objs['entities']:
        obj['box'] = compute_real_bbox(obj['box'], 1280, 720) 
        print(obj)

@log_time
def main():
    vlm = initialize_clients()

    obj_keys = "https://pub-kylin.tos-cn-beijing.volces.com/0003/304.mp4"

    process_videos(vlm, obj_keys)

if __name__ == "__main__":
    main()
