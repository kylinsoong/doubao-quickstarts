import os
import json
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time
import concurrent.futures
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize():

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")
    vlm = ByteVLM(api_key=api_key, model=model)

    prompt = load_file_content("prompt.risk.control.single.ini")

    data = [
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1001.jpeg",
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1002.jpeg",
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1003.jpeg",
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1004.jpeg",
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1005.jpeg",
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1006.jpeg",
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1007.jpeg",
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1008.jpeg",
        "https://pub-kylin.tos-cn-beijing.volces.com/8769/1009.jpeg"
    ]

    return vlm, prompt, data


@log_time
def process(vlm, prompt, url):
    content, usage = vlm.analyze_image(prompt=prompt, image_url=url, temperature=0.01)
    return content


@log_time
def main():

    logging.info("Visual Risk Control Start")

    vlm, prompt, data = initialize()
    contents = []

    # Use ThreadPoolExecutor to run process function concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        future_to_url = {executor.submit(process, vlm, prompt, url): url for url in data}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                content = future.result()
                json_content = json.loads(content)
                contents.append(json_content)
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(contents, f, ensure_ascii=False)

    logging.info("Visual Risk Control End")

if __name__ == "__main__":
    main()
