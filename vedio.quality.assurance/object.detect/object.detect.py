import os
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time
from byteLIB import generate_urls

def initialize_clients():


    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")

    vlm = ByteVLM(api_key=api_key, model=model)

    return vlm


def generate_prompt():
    prompt = load_file_content("prompt.object.detect.ini")
    return prompt

def process_videos(vlm, urls):
    for url in urls:
        prompt = generate_prompt()
        results = vlm.process(prompt=prompt, video_url=url, thinking="enabled")
        print(results)

@log_time
def main():
    vlm = initialize_clients()

    obj_keys = ["https://wzyt.tos-cn-shanghai.ivolces.com/CH1-20250206154045-20250206154241.mp4", "https://wzyt.tos-cn-shanghai.ivolces.com/CH1-20250209203225-20250209203423.mp4"]

    process_videos(vlm, obj_keys)

if __name__ == "__main__":
    main()
