from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import pandas as pd
import os
import requests
from io import BytesIO
from datetime import datetime
import tos
import tempfile
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    urls: str  # 保持为字符串类型
    skiprows: int

    @field_validator('urls')
    def validate_urls(cls, v):
        # 使用正则分割任意空白字符
        url_list = re.split(r'\s+', v.strip())
        if not url_list or not all(url_list):
            raise ValueError("至少需要提供一个有效的URL")
        return v

def clean_row(row):
    cleaned_values = list(dict.fromkeys([str(val) for val in row if pd.notna(val)])) 
    return " ".join(cleaned_values) if cleaned_values else ""

def get_tos_client():
    ak = os.getenv('TOS_ACCESS_KEY')
    sk = os.getenv('TOS_SECRET_KEY')
    endpoint = "tos-cn-beijing.volces.com"
    region = "cn-beijing"
    return tos.TosClientV2(ak, sk, endpoint, region)

@app.post("/process-excel")
async def process_excel(request: ProcessRequest):
    try:
        dfs = []
        dfs_headers = []
        
        # 分割URL字符串
        url_list = re.split(r'\s+', request.urls.strip())
        
        for idx, url in enumerate(url_list):
            try:
                # 添加URL基础验证
                if not url.startswith(('http://', 'https://')):
                    raise ValueError(f"无效的URL格式: {url}")
                    
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                # 添加文件类型验证
                if not response.headers.get('Content-Type', '').startswith(('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/octet-stream')):
                    raise ValueError("仅支持Excel文件")
                
                excel_data = BytesIO(response.content)
                df_full = pd.read_excel(excel_data, header=None)
                
                # 验证skiprows参数
                if request.skiprows >= len(df_full):
                    raise ValueError("skiprows值超过文件总行数")
                
                dfs_header = df_full.iloc[:request.skiprows]
                dfs_headers.append(dfs_header)
                
                df_data = df_full.iloc[request.skiprows:].reset_index(drop=True)
                if not df_data.empty:
                    columns = df_data.iloc[0].tolist()
                    df_data = df_data[1:]
                    df_data.columns = columns
                    if idx > 0:
                        df_data = df_data.iloc[:, 2:]
                    dfs.append(df_data)
                
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"处理 {url} 时出错: {str(e)}"
                )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'merged_{timestamp}.xlsx'
        
        combined_headers = pd.concat(dfs_headers, axis=1)
        cleaned_header_rows = combined_headers.apply(clean_row, axis=1)
        header_string = "\n".join(cleaned_header_rows.tolist())

        combined_df = pd.concat(dfs, axis=1) if dfs else pd.DataFrame()

        tos_client = get_tos_client()
        bucket_name = "pub-kylin"
        object_key = f"citic/{output_file}"
        
        try:
            with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
                combined_df.to_excel(temp_file.name, index=False, engine='openpyxl')
                
                # 添加文件大小验证
                file_size = os.path.getsize(temp_file.name)
                if file_size > 50 * 1024 * 1024:  # 50MB限制
                    raise ValueError("生成的文件过大")
                
                tos_client.put_object_from_file(
                    bucket=bucket_name,
                    key=object_key,
                    file_path=temp_file.name
                )
            
            return {
                "headers": header_string,
                "download_url": f"https://pub-kylin.tos-cn-beijing.volces.com/{object_key}"
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"文件上传失败: {str(e)}"
            )
        finally:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )
