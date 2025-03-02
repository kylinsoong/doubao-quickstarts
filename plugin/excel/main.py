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


urls = 'https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/ebec8c3ddfe04dcca1b1b36dfefcfd24.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743158134&x-signature=lpzyx8vheQRaIMZDpftJFlJwkYs%3D https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/e5f953e4aef545faa13d5ce1c5870a19.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743158134&x-signature=Sup3p8ZADmdkeCUOPcFWFrElcBA%3D https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/6522f52c1f4f40f287206654342e899e.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743158134&x-signature=2j0WhF845fRl5mj4bxZIDfavFAc%3D https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/e6675fc5ae3142f7bab1eca0c17b4136.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743158134&x-signature=%2B6b0HDibs8g%2FmDvEG2cv6ElvCaY%3D'


print(process_excel_urls(urls))

