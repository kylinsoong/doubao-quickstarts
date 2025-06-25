import os
import json
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time
from concurrent.futures import ThreadPoolExecutor
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize():

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")
    vlm = ByteVLM(api_key=api_key, model=model)

    prompt = load_file_content("prompt.person.detect.ini")

    return vlm, prompt


def process(vlm, prompt, url):
    try:
        content, usage = vlm.analyze_video(prompt=prompt, video_url=url, thinking="enabled", temperature=0.01)
        print(content)
        print(usage)
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")


@log_time
def execute():

    vlm, prompt = initialize()
    #url = "https://baoxian-crm.oss-accelerate.aliyuncs.com/momo_tracker_videos/1750774970_motion_video_6c69d36c-29ab-4a4e-91bb-82292229363d_1913753014424911873_1750773216.mp4"
    url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/1750773216.mp4"
    process(vlm, prompt, url)


if __name__ == "__main__":
    execute()
