import pandas as pd
import requests
from io import BytesIO
import json

def clean_header(header_rows):
    cleaned_header = []
    for row in header_rows:
        unique_values = list(dict.fromkeys(filter(lambda x: pd.notna(x) and x is not None and x != "", row)))
        if unique_values:  
            cleaned_header.append(unique_values)
    return cleaned_header



def handler(excels, header_rows):
    dfs = []
    for idx, url in enumerate(excels):
        try:
            response = requests.get(url)
            response.raise_for_status()
            excel_data = BytesIO(response.content)
            xls = pd.ExcelFile(excel_data)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                raw_headers = df.iloc[:header_rows].values.tolist()
                headers = clean_header(raw_headers)
                data = df.iloc[header_rows:].values.tolist()
                result = {
                    "header": headers,
                    "data": data,
                    "sheet": sheet_name, 
                    "file": url
                }
                dfs.append(str(result))
        except Exception as e:
            print(f"Error processing {url}: {e}")

    return dfs






excels = ["https://pub-kylin.tos-cn-beijing.volces.com/93368/20221231-margin.xlsx", "https://pub-kylin.tos-cn-beijing.volces.com/93368/20241130-margin.xlsx"]
header_rows = 3

result = handler(excels, header_rows)

for i in  result:
    print(i)
    print()

