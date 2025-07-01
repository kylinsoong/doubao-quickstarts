import os
import json
from byteLIB import ByteLLM
from byteLIB import load_file_content
from byteLIB import load_folder_content
from byteLIB import log_time
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

results = []

def initialize():

    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_API_ENGPOINT_ID")
    llm = ByteLLM(api_key=api_key, model=model)

    prompt = load_file_content("prompt.complaint.warning.upgrade.ini")

    inputs = load_folder_content("./role")
  
    return llm, prompt, inputs


def process(llm, prompt, item):

    user_prompt = prompt.replace('{{COLLECTION_CONVERSATION}}', item[1])
    
    try:
        content, usage = llm.analyze(prompt=user_prompt, temperature=0.01, max_tokens=16000)
        message = json.loads(content)
        item.append(message)
        results.append(item)
        logging.info(f"LLM Usage: prompt tokens={usage.prompt_tokens}, "
                     f"completion tokens={usage.completion_tokens}, "
                     f"total tokens={usage.total_tokens}")
    except Exception as e:
        logging.error(f"Error {e}")



@log_time
def execute():

    llm, prompt, data = initialize()

    num_threads = 20
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process, llm, prompt, item) for item in data]

        for future in futures:
            future.result()


def main():
    execute()

    output = "warning_upgrade"
    os.makedirs(output, exist_ok=True)
    for item in results:
        file_path = os.path.join(output, item[0])
        with open(file_path, 'w', encoding='utf-8') as file:
            json_content = json.dumps(item[2], ensure_ascii=False, indent=2)
            file.write(json_content)
        logging.info(f"Successfully created file: {file_path}")

if __name__ == "__main__":
    main()

