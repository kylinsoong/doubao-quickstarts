import os
import time
import json
import logging
import openpyxl

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper


def load_json_value(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_json(file_path):
    #with open(file_path, 'r', encoding='utf-8') as f:
    #    return json.load(f)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def form_file_path(id, folder):
    file_path = f"{folder}/{id}.json"
    return file_path

@log_time
def main(json_path):
    data = load_json_value(json_path)
    rows = []
    for idx, item in enumerate(data, 1):
        id = item['id']
        audio = item['audio']
        input = load_json(form_file_path(id, "input"))
        role = load_json(form_file_path(id, "role"))
        results = load_json(form_file_path(id, "results"))
        huankuan = load_json(form_file_path(id, "huankuan"))
        complaint = load_json(form_file_path(id, "complaint"))
        intent = load_json(form_file_path(id, "intent"))
        sentiment = load_json(form_file_path(id, "sentiment"))
        sentiment_summary = load_json(form_file_path(id, "sentiment_summary"))
        abnormal = load_json(form_file_path(id, "abnormal"))
        form = load_json(form_file_path(id, "form"))
        figure = load_json(form_file_path(id, "figure"))
        rows.append((id, audio, input, role, results, huankuan, complaint, sentiment, sentiment_summary, abnormal, form, figure))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test_Excel"

    ws.append(["语音样本编号", "语音样本名称", "ASR 结果", "角色设定", "质检结果", "还款意愿", "投诉意愿", "逐句情感分析", "情感分析总结", "异常检测", "工单填写", "客服画像"])        
 
    for row in rows:
        ws.append(row)

    wb.save("test_excel.xlsx")

    print("Excel file saved")

if __name__ == "__main__":
    json_path = "object_samples.json"
    main(json_path)
