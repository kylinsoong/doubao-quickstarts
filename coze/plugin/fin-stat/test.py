import pandas as pd
import requests
from io import BytesIO
import json


def clean_header(header_rows):
    """Remove duplicate values, None, and NaN from header rows."""
    cleaned_header = []
    for row in header_rows:
        unique_values = list(dict.fromkeys(filter(lambda x: pd.notna(x) and x is not None and x != "", row)))
        if unique_values:  # Only keep non-empty rows
            cleaned_header.append(unique_values)
    return cleaned_header

def process_excel(urls, header_rows):
    url_array = urls.split()
    dfs = []
    for idx, url in enumerate(url_array):
        try:
            response = requests.get(url)
            response.raise_for_status()
            excel_data = BytesIO(response.content)
            df = pd.read_excel(excel_data, header=None)
            raw_headers = df.iloc[:header_rows].values.tolist()
            headers = clean_header(raw_headers)
            data = df.iloc[header_rows:].values.tolist()
            result = {
                "header": headers,
                "data": data,
                "file": url
            }
            dfs.append(result)
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)
    return json.dumps(dfs, ensure_ascii=False)
        

urls = 'https://pub-kylin.tos-cn-beijing.volces.com/0001/01/20221231-margin.xlsx https://pub-kylin.tos-cn-beijing.volces.com/0001/01/20231231-margin.xlsx https://pub-kylin.tos-cn-beijing.volces.com/0001/01/20241130-margin.xlsx'
results = process_excel(urls, 3)

print(results)
