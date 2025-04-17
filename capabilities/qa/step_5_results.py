import json
import os

def extract_utterances(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        result = data['result']
        results = []
        if 'utterances' in result:
            utterances = result['utterances']
            for item in utterances:
                start_time = round(item['start_time'] / 1000, 2)
                end_time = round(item['end_time'] / 1000, 2)
                interval = f"{start_time} - {end_time}"
                utterance = {
                    "role": f"speaker-{item['additions']['speaker']}",
                    "time": interval,
                    "text": item['text']
                } 
                results.append(utterance)

        target = file_path.replace(".asr", ".input")
        with open(target, 'w') as file:
            json.dump(results, file, ensure_ascii=False)
        print("add ", target)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查文件路径。")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 存在 JSON 解析错误，请检查文件格式。")
    return None

def list_files_and_extract(dir_path):
    if not os.path.isdir(dir_path):
        print(f"{dir_path} 不是一个有效的目录。")
        return

    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            #print(f"处理文件: {file_path}")
            extract_utterances(file_path)

if __name__ == "__main__":
    directory = '.asr'  
    list_files_and_extract(directory)
