import pandas as pd
import json
from pathlib import Path

def excel_to_json(excel_file: str, output_file: str = None, indent: int = 2) -> dict:
    """
    将Excel文件转换为JSON格式
    
    参数:
    excel_file (str): Excel文件路径
    output_file (str, optional): 输出JSON文件路径。如果为None，则返回JSON字符串
    indent (int, optional): JSON缩进空格数，默认为2
    
    返回:
    dict: 转换后的JSON数据
    """
    try:
        # 读取Excel文件
        excel_file = Path(excel_file)
        if not excel_file.exists():
            raise FileNotFoundError(f"文件不存在: {excel_file}")
            
        # 使用pandas读取Excel文件
        xls = pd.ExcelFile(excel_file)
        
        # 获取所有表名
        sheet_names = xls.sheet_names
        result = {}
        
        # 处理每个工作表
        for sheet_name in sheet_names:
            # 读取工作表数据
            df = xls.parse(sheet_name)
            
            # 处理缺失值
            df = df.fillna('nan')
            
            # 将DataFrame转换为字典列表
            data = df.to_dict(orient='records')
            
            # 添加到结果中
            result[sheet_name] = data
        
        # 如果指定了输出文件，则保存为JSON文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=indent)
            print(f"已成功将Excel文件转换为JSON并保存至: {output_file}")
        
        return result
    
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")
        return None

def main():

    input = "/Users/bytedance/Downloads/zj_new.xlsx"
    output = "convert.json"
    indent = 2    

    result = excel_to_json(input, output, indent)
    
    if result and not output:
        print(json.dumps(result, ensure_ascii=False, indent=indent))

if __name__ == "__main__":
    main()    
