import os
from byteLIB import ByteTOS
from byteLIB import ByteVideoASR
from byteLIB import ByteVLM
from byteLIB import load_file_content

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket = os.getenv('TOS_BUCKET')

appid = os.getenv("X_API_APPID")
access_token = os.getenv("X_API_TOKEN")

api_key = os.environ.get("ARK_API_KEY")
model = os.environ.get("ARK_API_ENGPOINT_ID")

original_prompt = load_file_content("prompt.caption.syn.check.ini")

tos = ByteTOS(ak=ak, sk=sk, endpoint=endpoint, region=region, bucket=bucket)
asr = ByteVideoASR(appid=appid, access_token=access_token)
vlm = ByteVLM(api_key=api_key,model=model)

#obj_keys = ["qsmutual/020.mp4", "qsmutual/021.mp4"]
obj_keys = ["qsmutual/021.mp4"]

urls = tos.generate_signed_urls(obj_keys)

for url in urls:
    asr_results = asr.process(url)
    prompt = original_prompt.replace("{{ASR_JSON_SUBTITLES}}", asr_results)
    results = vlm.process(prompt=prompt,video_url=url)
    print(results)
