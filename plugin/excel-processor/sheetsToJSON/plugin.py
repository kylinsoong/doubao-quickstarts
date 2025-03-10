from runtime import Args
from typings.sheetsToJSON.sheetsToJSON import Input, Output
import pandas as pd
import requests
from io import BytesIO

def clean_header(header_rows):
    cleaned_header = []
    for row in header_rows:
        unique_values = list(dict.fromkeys(filter(lambda x: pd.notna(x) and x is not None and x != "", row)))
        if unique_values:
            cleaned_header.append(unique_values)
    return cleaned_header

"""
Each file needs to export a function named `handler`. This function is the entrance to the Tool.

Parameters:
args: parameters of the entry function.
args.input - input parameters, you can get test input value by args.input.xxx.
args.logger - logger instance used to print logs, injected by runtime.

Remember to fill in input/output in Metadata, it helps LLM to recognize and use tool.

Return:
The return data of the function, which should match the declared output parameters.
"""
def handler(args: Args[Input])->Output:

    excels = args.input.excels
    header_rows = args.input.header_rows
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


    return {"results": dfs}
