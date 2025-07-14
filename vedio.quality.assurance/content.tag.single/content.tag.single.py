import os
from byteLIB import ByteTOS
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time
from byteLIB import generate_urls

def initialize_clients():

    ak = os.getenv('TOS_ACCESS_KEY')
    sk = os.getenv('TOS_SECRET_KEY')
    endpoint = os.getenv('TOS_ENDPOINT')
    region = os.getenv('TOS_REGION')
    bucket = os.getenv('TOS_BUCKET')

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")

    tos = ByteTOS(ak=ak, sk=sk, endpoint=endpoint, region=region, bucket=bucket)
    vlm = ByteVLM(api_key=api_key, model=model)

    return tos, vlm


def generate_prompt():
    prompt = load_file_content("prompt.content.tag.single.ini")
    return prompt

def process_videos(tos, vlm, obj_keys):
    urls = generate_urls(obj_keys)
    for url in urls:
        prompt = generate_prompt()
        results = vlm.process(prompt=prompt, video_url=url, thinking="enabled")
        print(results)

@log_time
def main():
    tos, vlm = initialize_clients()

    obj_keys = ["0003/331_1741769819.mp4", "0003/333_1741769846.mp4", "0003/340_1741769995.mp4", "0003/345_1741770061.mp4", "0003/351_1741770662.mp4", "0003/354_1741770778.mp4", "0003/357_1741771539.mp4"]

    process_videos(tos, vlm, obj_keys)

if __name__ == "__main__":
    main()
