import os
from byteLIB import ByteTOS
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time

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


def process_videos(tos, vlm, obj_keys):
    urls = tos.generate_signed_urls(obj_keys)
    for url in urls:
        prompt = load_file_content("prompt.caption.font.check.test.ini")
        results = vlm.process(prompt=prompt, video_url=url, thinking="enabled")
        print(results)

@log_time
def main():
    tos, vlm = initialize_clients()

    obj_keys = ["qsmutual/021.mp4"]

    process_videos(tos, vlm, obj_keys)

if __name__ == "__main__":
    main()
