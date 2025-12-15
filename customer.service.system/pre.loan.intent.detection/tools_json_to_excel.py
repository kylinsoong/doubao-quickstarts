import os
import json
import pandas as pd

def read_json_files_from_path(path):
    json_contents = []
    
    if not os.path.exists(path):
        print(f"错误: 路径 '{path}' 不存在")
        return json_contents
    
    if not os.path.isdir(path):
        print(f"错误: '{path}' 不是一个目录")
        return json_contents
    
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            file_path = os.path.join(path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        json_data = json.load(file)
                        json_contents.append({
                            'filename': filename,
                            'content': json_data
                        })
                    except json.JSONDecodeError:
                        print(f"错误: 文件 '{filename}' 不是有效的JSON格式")
                    except Exception as e:
                        print(f"处理文件 '{filename}' 时出错: {str(e)}")
            except IOError as e:
                print(f"无法打开文件 '{filename}': {str(e)}")
    
    return json_contents


def export_to_excel(json_files, output_file="output.xlsx"):
    # 准备Excel数据
    excel_data = []
    
    for item in json_files:
        content = item['content']
        filename = item['filename']  # 获取文件名用于错误提示
        
        # 提取所需字段，处理可能的缺失值
        audio = content.get('audio', '')
        asr = content.get('asr', [])
        asr_str = json.dumps(asr, ensure_ascii=False, indent=2)
        
        # 处理tag字段，增加类型检查
        tag = content.get('tag', {})
        # 检查tag是否为字典类型
        if isinstance(tag, dict):
            tag_tag = tag.get('tag', '')
            tag_reason = tag.get('reason', '')
        else:
            # 如果tag不是字典，将其作为tag值，reason留空
            print(f"警告: 文件 '{filename}' 中的tag不是字典类型，值为: {tag}")
            tag_tag = str(tag)  # 转换为字符串
            tag_reason = ""
        
        # 添加到数据列表
        excel_data.append({
            'audio': audio,
            'asr': asr_str,
            'tag.tag': tag_tag,
            'tag.reason': tag_reason
        })
    
    # 创建DataFrame并导出到Excel
    df = pd.DataFrame(excel_data)
    df.to_excel(output_file, index=False)
    print(f"成功导出 {len(excel_data)} 条数据到 {output_file}")

def export_to_excel_old(json_files, output_file="output.xlsx"):
    # 准备Excel数据
    excel_data = []
    
    for item in json_files:
        content = item['content']
        
        # 提取所需字段，处理可能的缺失值
        audio = content.get('audio', '')
        asr = content.get('asr', [])
        # 将asr列表转换为字符串以便在Excel中显示
        asr_str = json.dumps(asr, ensure_ascii=False, indent=2)
        
        tag = content.get('tag', {})
        tag_tag = tag.get('tag', '')
        tag_reason = tag.get('reason', '')
        
        # 添加到数据列表
        excel_data.append({
            'audio': audio,
            'asr': asr_str,
            'tag.tag': tag_tag,
            'tag.reason': tag_reason
        })
    
    # 创建DataFrame并导出到Excel
    df = pd.DataFrame(excel_data)
    df.to_excel(output_file, index=False)
    print(f"成功导出 {len(excel_data)} 条数据到 {output_file}")

if __name__ == "__main__":

    target_path = "/Users/bytedance/Downloads/result"  # 替换为你的JSON文件所在路径
    #target_path = "result"    

    if not os.path.exists(target_path):
        os.makedirs(target_path)
        print(f"创建了目录: {target_path}")
    
    json_files = read_json_files_from_path(target_path)
    
    export_to_excel(json_files)

    
