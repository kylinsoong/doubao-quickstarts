import pandas as pd
import requests
from io import BytesIO
import json
from datetime import datetime

def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  
    raise TypeError(f"Type {obj.__class__.__name__} not serializable")

def process_excel_urls(urls):
    result = []
    url_array = urls.split()
    for url in url_array:
        response = requests.get(url)
        response.raise_for_status()
        excel_data = BytesIO(response.content)
        dfs = pd.read_excel(excel_data, sheet_name=None)
        for sheet_name, df in dfs.items():
            df = df.dropna()
            sheet_object = {
               'name': sheet_name,
                'value': df.to_dict(orient='records')
            }
            result.append(sheet_object)

    return json.dumps(result, indent=2,default=convert_datetime, ensure_ascii=False)


urls = 'https://pub-kylin.tos-cn-beijing.volces.com/0001/02/2023-11yzxl.xlsx https://pub-kylin.tos-cn-beijing.volces.com/0001/02/2023.11jsxn.xlsx https://pub-kylin.tos-cn-beijing.volces.com/0001/02/20241130bhly.xlsx https://pub-kylin.tos-cn-beijing.volces.com/0001/02/20241130ngjt.xlsx'

print(process_excel_urls(urls))

