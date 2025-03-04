from fastapi import FastAPI
import pandas as pd
import requests
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/api/citic")
def read_citic():
    return {"message": "CITIC API"}

def clean_header(header_rows):
    cleaned_header = []
    for row in header_rows:
        unique_values = list(dict.fromkeys(filter(lambda x: pd.notna(x) and x is not None and x != "", row)))
        if unique_values:  # Only keep non-empty rows
            cleaned_header.append(unique_values)
    return cleaned_header

@app.get("/api/citic/excelToJson")
def process_excel(urls, header_rows: int):
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
            return "{}"
    return dfs
