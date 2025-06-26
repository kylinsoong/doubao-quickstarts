import json

def clean_collection_data(input_data):
    """
    清洗催收记录数据，转换字段名称并仅保留数组部分
    
    参数:
    input_data (dict): 包含催收记录的原始数据
    
    返回:
    list: 清洗后的催收记录列表
    """
    records = input_data.get("query-hive-2290492", [])
    
    field_mapping = {
        "no": "id",
        "llm_output_text": "message",
        "发给本人违规原因": "reason",
        "发送本人违规等级": "level",
        "发送本人违规类别": "category"
    }
    
    cleaned_records = []
    for record in records:
        cleaned_record = {}
        for old_key, new_key in field_mapping.items():
            if old_key in record:
                cleaned_record[new_key] = record[old_key]
        cleaned_records.append(cleaned_record)
    
    return cleaned_records

if __name__ == "__main__":

    with open('convert.json', 'r', encoding='utf-8') as file:
        file_contents = file.read()

    raw_data = json.loads(file_contents)
    
    cleaned_data = clean_collection_data(raw_data)
    
    print(json.dumps(cleaned_data, ensure_ascii=False, indent=2))    

    output_file = "clean.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    print(f"Cleaned JSON Saved as: {output_file}")
