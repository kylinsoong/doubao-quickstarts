import os
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time
from byteLIB import generate_urls
import json

def initialize_clients():


    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")

    vlm = ByteVLM(api_key=api_key, model=model)

    return vlm


def generate_prompt():
    prompt = load_file_content("prompt.object.detect.prededefine.ini")
    return prompt

def compute_real_bbox(bbox_str, video_width, video_height):
        """
        Calculate real bounding box coordinates from thousandth-scale values
        and return as a space-separated string.
        
        Args:
            bbox_str (str): Bounding box string in format "x_min y_min x_max y_max"
            video_width (int): Original video width (e.g., 3840)
            video_height (int): Original video height (e.g., 2160)
        
        Returns:
            str: Real coordinates as "x_min y_min x_max y_max" string
        """
        # Parse the bbox string into individual components
        x_min, y_min, x_max, y_max = map(int, bbox_str.split())
        
        # Calculate real coordinates using thousandth scale conversion
        real_x_min = int(x_min * video_width / 1000)
        real_y_min = int(y_min * video_height / 1000)
        real_x_max = int(x_max * video_width / 1000)
        real_y_max = int(y_max * video_height / 1000)
        
        # Return as space-separated string
        return f"{real_x_min} {real_y_min} {real_x_max} {real_y_max}"



def process_videos(vlm, urls):
    for url in urls:
        prompt = generate_prompt()
        results = vlm.process(prompt=prompt, video_url=url, thinking="enabled", max_tokens=32000)
        objs_array = json.loads(results)
        for obj in objs_array:
            obj['bbox'] = compute_real_bbox(obj['bbox'], 3840, 2160)
            print(obj)

@log_time
def main():
    vlm = initialize_clients()

    obj_keys = ["https://pub-kylin.tos-cn-beijing.volces.com/0003/302.mp4"]

    process_videos(vlm, obj_keys)

if __name__ == "__main__":
    main()
