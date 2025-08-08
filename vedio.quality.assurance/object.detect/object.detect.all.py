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
    prompt = load_file_content("prompt.object.scene.ini")
    return prompt

def process_videos(vlm, urls):
    for url in urls:
        prompt = generate_prompt()
        results = vlm.process(prompt=prompt, video_url=url, thinking="enabled")
        print(results)

def process_video_scene(vlm, url):
    prompt = generate_prompt()
    results = vlm.process(prompt=prompt, video_url=url)
    return results

@log_time
def main():
    vlm = initialize_clients()
    url = "https://pub-kylin.tos-cn-beijing.volces.com/0003/301.mp4"
    scene = process_video_scene(vlm, url)

    print(scene)

if __name__ == "__main__":
    main()
