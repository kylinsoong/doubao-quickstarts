import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
import concurrent.futures  
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_prompt_from_file(file_path="prompt.loan.tag.1.ini"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()  
    except FileNotFoundError:
        logging.error(f"提示词文件 {file_path} 未找到，请检查路径是否正确")
        raise  
    except Exception as e:
        logging.error(f"读取提示词文件失败: {e}")
        raise

original_prompt = load_prompt_from_file()

API_KEY = os.environ.get("ARK_API_KEY")
models = [os.environ.get("ARK_API_ENGPOINT_ID_1")]


def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' ran in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper


def execute(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            collection_dialog = json.load(file)
        prompt = original_prompt.replace("{{input}}", json.dumps(collection_dialog, ensure_ascii=False))
    except FileNotFoundError:
        logging.error(f"错误: 文件 {filepath} 未找到。")
        return
    except json.JSONDecodeError:
        logging.error(f"错误: 无法解析 {filepath} 中的JSON数据。")
        return
    except Exception as e:
        logging.error(f"文件处理未知错误 [{filepath}]: {e}")
        return

    try:
        client = Ark(api_key=API_KEY)
        completion = client.chat.completions.create(
            model=random.choice(models),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=16000
        )
    except Exception as e:  
        logging.error(f"API调用失败 [{filepath}]: {e}")
        return

    try:
        message = completion.choices[0].message.content
        usage = completion.usage
        if not (message and usage):
            logging.warning(f"API返回空结果 [{filepath}]")
            return

        target = filepath.replace("role", "loan")
        try:
            json_obj = json.loads(message)
        except json.JSONDecodeError:
            json_obj = message  

        with open(target, 'w', encoding='utf-8') as file:
            json.dump(json_obj, file, ensure_ascii=False, indent=2)
        logging.info(f"处理完成 [{filepath}]，结果写入: {target}，使用情况: {usage}")
    except Exception as e:
        logging.error(f"结果处理失败 [{filepath}]: {e}")
        return


@log_time
def main(folder):
    json_files = [
        os.path.join(folder, f) 
        for f in os.listdir(folder) 
        if f.endswith('.json') and os.path.isfile(os.path.join(folder, f))  
    ]
    logging.info(f"共发现 {len(json_files)} 个JSON文件待处理")

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(execute, filepath): filepath for filepath in json_files}
        
        for future in concurrent.futures.as_completed(futures):
            filepath = futures[future]
            try:
                future.result()  
            except Exception as e:
                logging.error(f"任务执行异常 [{filepath}]: {e}")


if __name__ == "__main__":
    folder = "role"
    main(folder)
