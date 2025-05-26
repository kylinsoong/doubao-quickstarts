import pandas as pd
import os
import requests
from io import BytesIO
from datetime import datetime
import tos
import tempfile

def clean_row(row):
    cleaned_values = list(dict.fromkeys([str(val) for val in row if pd.notna(val)])) 
    return " ".join(cleaned_values) if cleaned_values else ""

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')


def process_excel_urls(urls, skiprows):    
    url_array = urls.split()
    dfs = []
    dfs_headers = []
    for idx, url in enumerate(url_array):
        try:
            response = requests.get(url)
            response.raise_for_status()
            excel_data = BytesIO(response.content)
            df_full = pd.read_excel(excel_data, header=None)
            dfs_header = df_full.iloc[:skiprows]
            dfs_headers.append(dfs_header)
            df_data = df_full.iloc[skiprows:].reset_index(drop=True)
            if not df_data.empty:
                columns = df_data.iloc[0].tolist()
                df_data = df_data[1:]
                df_data.columns = columns
                if idx > 0:
                    df_data = df_data.iloc[:, 2:]
                dfs.append(df_data)
            else:
                dfs.append(pd.DataFrame())
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'merged_{timestamp}.xlsx'

    if dfs and dfs_headers:
        combined_headers = pd.concat(dfs_headers, axis=1)
        cleaned_header_rows = combined_headers.apply(clean_row, axis=1)
        header_string = "\n".join(cleaned_header_rows.tolist())

        combined_df = pd.concat(dfs, axis=1)

        endpoint = "tos-cn-beijing.volces.com"
        region = "cn-beijing"
        bucket_name = "pub-kylin"
        tos_client = tos.TosClientV2(ak, sk, endpoint, region)
        base_path = "citic"
        object_key = os.path.join(base_path, output_file)
        final_path = "https://pub-kylin.tos-cn-beijing.volces.com/" + object_key
    
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
            temp_filename = temp_file.name
            combined_df.to_excel(temp_filename, index=False)
            try:
                result = tos_client.put_object_from_file(bucket_name, object_key, temp_filename)
                print(header_string)
                print(final_path)
            except Exception as e:
                print(f"Error saving file: {e}")


