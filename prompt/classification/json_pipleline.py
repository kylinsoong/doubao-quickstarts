import os
import json


prefix = "我下面发你的内容可能是多人对话，也有可能是一个人在说话，请按规则给出答案：如果是采访对话内容（存在有一个人向多人问类似问题；或者两人中一人先向另一人提出问题，然后提问者主导话题继续交流。尤其是这些人关系并非亲友），则你的回答应该是“采访类”；如果是多个人讨论某一个话题（尤其是这几个人关系像是亲友），则你的回答应该是”情景剧“；如果不是以上两种，则请你回答应该是“其他”。内容是："

try:
    with open("sample.json", 'r', encoding='utf-8') as file:
        data_list = json.load(file)
except FileNotFoundError:
    print(f"文件 {json_file_path} 未找到，请检查文件路径是否正确。")
except json.JSONDecodeError:
    print(f"文件 {json_file_path} 不是有效的 JSON 格式，请检查文件内容。")

new_data = []
output_file_path = "cleaned_data.json"

for data in data_list:
    id = data['id']
    text = data['prompt'].removeprefix(prefix)
    label = data['正确回答']
    new_data.append({"id": id, "text": text, "label": label})

with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(new_data, outfile, ensure_ascii=False, indent=4)

print(f"新文件已保存: {output_file_path}")
