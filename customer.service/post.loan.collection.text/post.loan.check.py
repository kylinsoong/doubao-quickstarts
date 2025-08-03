import os
import json
from byteLIB import ByteLLM
from byteLIB import load_file_content
from byteLIB import log_time
from concurrent.futures import ThreadPoolExecutor
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

results = []

def initialize():

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")
    llm = ByteLLM(api_key=api_key, model=model)

    prompt = load_file_content("prompt.collection.sms.labeling.ini")

    content = load_file_content("clean.json")

    data = json.loads(content)

    return llm, prompt, data


def process(llm, prompt, message):
    user_prompt = prompt.replace("{{COLLECTION_MESSAGE}}", message['message'])
    try:
        content, usage = llm.analyze(prompt=user_prompt, thinking="enabled", temperature=0.01)
#        print(content)
        message['llm'] = json.loads(content)
        results.append(message)
    except Exception as e:
        logging.error(f"Error {e}")


@log_time
def execute():

    logging.info("Start")

    llm, prompt, data = initialize()

    num_threads = 30
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process, llm, prompt, message) for message in data]

        for future in futures:
            future.result()

    logging.info("End")



def main():

    execute()

    sorted_data = sorted(results, key=lambda x: x['id'])

    output_file_path = "output.json"
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)

    logging.info("Result written to file: %s", output_file_path)




if __name__ == "__main__":
    main()
