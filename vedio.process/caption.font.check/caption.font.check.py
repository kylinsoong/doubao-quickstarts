import os
from byteLIB import ByteTOS
from byteLIB import ByteVideoASR
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time

def initialize_clients():

    ak = os.getenv('TOS_ACCESS_KEY')
    sk = os.getenv('TOS_SECRET_KEY')
    endpoint = os.getenv('TOS_ENDPOINT')
    region = os.getenv('TOS_REGION')
    bucket = os.getenv('TOS_BUCKET')

    appid = os.getenv("X_API_APPID")
    access_token = os.getenv("X_API_TOKEN")

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")

    tos = ByteTOS(ak=ak, sk=sk, endpoint=endpoint, region=region, bucket=bucket)
    asr = ByteVideoASR(appid=appid, access_token=access_token)
    vlm = ByteVLM(api_key=api_key, model=model)

    return tos, asr, vlm


def generate_prompt(asr_results):
    original_prompt = load_file_content("prompt.caption.font.check.ini")
    prompt = original_prompt.replace("{{ASR_JSON_SUBTITLES}}", asr_results)
    return prompt

def process_videos(tos, asr, vlm, obj_keys):
    urls = tos.generate_signed_urls(obj_keys)
    for url in urls:
        asr_results = asr.process(url)
        prompt = generate_prompt(asr_results)
        results = vlm.process(prompt=prompt, video_url=url, thinking="enabled")
        print(results)

@log_time
def main():
    tos, asr, vlm = initialize_clients()

    #obj_keys = ["qsmutual/020.mp4", "qsmutual/021.mp4"]
    obj_keys = ["qsmutual/021.mp4"]

    process_videos(tos, asr, vlm, obj_keys)

if __name__ == "__main__":
    main()
