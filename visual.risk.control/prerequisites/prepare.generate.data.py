import os
from byteLIB import ByteVLM
from byteLIB import load_file_content
import json
from concurrent.futures import ThreadPoolExecutor
from byteLIB import log_time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

results = []

def initialize():

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")
    vlm = ByteVLM(api_key=api_key, model=model)

    prompt = load_file_content("prompt.prepare.generate.data.ini")

    return vlm, prompt


def process(vlm, prompt, url):
    try:
        content, usage = vlm.analyze_image(prompt=prompt, image_url=url, thinking="disabled", temperature=0.01)
        json_content = json.loads(content)
        json_content['face'] = url
        results.append(json_content)
        logging.info(f"Processed {url} successfully. Usage: {usage}")
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")

@log_time
def main():
    vlm, prompt = initialize()
    base_url = "https://pub-kylin.tos-cn-beijing.volces.com/8769/"
    urls = [f"{base_url}{num}.jpeg" for num in range(1001, 1201)]

    num_threads = 30
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process, vlm, prompt, url) for url in urls]

        for future in futures:
            future.result()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
