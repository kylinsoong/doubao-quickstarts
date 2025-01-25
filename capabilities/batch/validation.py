import json

def check_jsonl_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        total = 0
        custom_id_set = set()
        for line in file:
            if line.strip() == "":
                continue
            try:
                line_dict = json.loads(line)
            except json.decoder.JSONDecodeError:
                raise Exception(f"批量推理输入文件格式错误，第{total+1}行非json数据")
            if not line_dict.get("custom_id"):
                raise Exception(f"批量推理输入文件格式错误，第{total+1}行custom_id不存在")
            if line_dict.get("custom_id") in custom_id_set:
                raise Exception(
                    f"批量推理输入文件格式错误，custom_id={line_dict.get('custom_id', '')}存在重复"
                )
            else:
                custom_id_set.add(line_dict.get("custom_id"))
            if not isinstance(line_dict.get("body", ""), dict):
                raise Exception(
                    f"批量推理输入文件格式错误，custom_id={line_dict.get('custom_id', '')}的body非json字符串"
                )
            total += 1
    return total


file_path = "task.jsonl"
total_lines = check_jsonl_file(file_path)
print(f"文件中有效 JSON 数据的行数为: {total_lines}")
