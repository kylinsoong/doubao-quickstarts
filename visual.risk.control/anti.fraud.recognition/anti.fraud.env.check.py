import os
import json
import random
from itertools import combinations
from byteLIB import ByteVLM
from byteLIB import load_file_content
from byteLIB import log_time
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

results = []

def random_select_combinations(input_list, number):
    if len(input_list) < 2:
        return []  

    all_combinations = list(combinations(input_list, 2))
    
    number = min(number, len(all_combinations)) 
    selected = random.sample(all_combinations, number)
    
    return selected


def initialize():

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")
    vlm = ByteVLM(api_key=api_key, model=model)

    prompt = load_file_content("prompt.anti.fraud.env.check.ini")

    content = load_file_content("../data/data-env.json")

    raw_list = json.loads(content)
    data = random_select_combinations(raw_list, 10)
  
    return vlm, prompt, data


def process(vlm, prompt, pair):
    image_pair = (pair[0]['face'], pair[1]['face'])
    try:
        content, usage = vlm.analyze_image_pair(prompt=prompt, pair=image_pair, thinking="disabled", temperature=0.01)
        result = json.loads(content)
        if result['tag'] == "是":
            for i in [0, 1]:
                other = pair[1 - i]['name']
                if 'reference' not in pair[i] or not isinstance(pair[i]['reference'], list):
                    pair[i]['reference'] = [other]
                else:
                    if other not in pair[i]['reference']:
                        pair[i]['reference'].append(other)

           # pair[0]['reference'] = pair[1]['name'] 
           # pair[1]['reference'] = pair[0]['name'] 

        results.append(pair)

        #logging.info(f"Processed {person['face']} successfully. Usage: {usage}")
    except Exception as e:
        logging.error(f"Error {e}")


@log_time
def execute():

    vlm, prompt, data = initialize()

    num_threads = 10
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process, vlm, prompt, pair) for pair in data]

        for future in futures:
            future.result()


def main():
    execute()

    output_file_path = "output.json"
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logging.info("Result written to file: %s", output_file_path)

if __name__ == "__main__":
    main()

