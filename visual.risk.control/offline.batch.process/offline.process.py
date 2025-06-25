import os
import json
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time
from concurrent.futures import ThreadPoolExecutor
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

results = []

def initialize():

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")
    vlm = ByteVLM(api_key=api_key, model=model)

    prompt = load_file_content("prompt.risk.control.single.ini")

    content = load_file_content("../data/data.json")

    data = json.loads(content)

    return vlm, prompt, data


def process(vlm, prompt, person):
    try:
        content, usage = vlm.analyze_image(prompt=prompt, image_url=person['face'], thinking="enabled", temperature=0.01)
        person['vlm'] = json.loads(content)
        results.append(person)
        #logging.info(f"Processed {person['face']} successfully. Usage: {usage}")
    except Exception as e:
        logging.error(f"Error processing {person['face']}: {e}")


@log_time
def execute():

    logging.info("Visual Risk Control Start")

    vlm, prompt, data = initialize()

    num_threads = 30
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process, vlm, prompt, person) for person in data]

        for future in futures:
            future.result()

    logging.info("Visual Risk Control End")


def main():

    execute()

    if not os.path.exists('output'):
        os.makedirs('output')

    for p in results:
        url = p['face']
        filename = url.split('/')[-1]        # '1197.jpeg'
        id_part = filename.split('.')[0]
        output_file_path = os.path.join('output', id_part + ".json")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(p, f, ensure_ascii=False)


 

if __name__ == "__main__":
    main()
