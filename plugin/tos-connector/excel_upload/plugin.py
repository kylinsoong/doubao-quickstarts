from runtime import Args
from typings.excel_upload.excel_upload import Input, Output
from urllib.parse import urlparse
import tos
import requests
import os
import tempfile
import zipfile

def extract_filename(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = path.split("/")[-1].split("~")[0]
    return filename


def process_xlsx(url, filename, endpoint, region, bucket_name, base_path, ak, sk, xlsx_files):
    object_key = os.path.join(base_path, filename)
    errorMessage = None
    client = tos.TosClientV2(ak, sk, endpoint, region)

    try:
        content = requests.get(url)
        client.put_object(bucket_name, object_key, content=content)
        content.close()
        target = f"https://{bucket_name}.{endpoint}/{object_key}"
        xlsx_files.append(target)
    except Exception as e:
        errorMessage = 'error: {}'.format(e)

    return errorMessage


def process_zip(url, filename, xlsx_files, unknown_files, endpoint, region, bucket_name, base_path, ak, sk):
    errorMessage = None
    client = tos.TosClientV2(ak, sk, endpoint, region)

    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, filename)
        print(zip_path)
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file == filename or file.startswith(".") or file.startswith("~") or "._" in file:
                        continue
                    print(file, type(file))
                    if file.endswith(".xlsx"):
                        file_path = os.path.join(root, file)
                        object_key = os.path.join(base_path, file)
                        with open(file_path, 'rb') as f:
                            client.put_object(bucket_name, object_key, content=f)
                        target = f"https://{bucket_name}.{endpoint}/{object_key}"
                        xlsx_files.append(target)
                    else:
                        unknown_files.append(file)

        except Exception as e:
            errorMessage = f'Error processing ZIP {filename}: {e}'

    return errorMessage

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

    urls = args.input.urls
    endpoint = args.input.endpoint
    region = args.input.region
    bucket_name = args.input.bucket_name
    base_path = args.input.base_path
    ak = args.input.ak
    sk = args.input.sk

    zip_files = []
    xlsx_files = []
    unknown_files = []
    errors = []

    if " " not in urls and ",http" in urls:
        url_array = urls.split(",")
    else:
        url_array = urls.split()

    for url in url_array:
        filename = extract_filename(url)
        if filename.endswith(".zip"):
            errorMessage = process_zip(url, filename, xlsx_files, unknown_files, endpoint, region, bucket_name, base_path, ak, sk)
            if errorMessage is not None:
                errors.append(errorMessage)
            else:
                zip_files.append(filename)
        elif filename.endswith(".xlsx"):
            errorMessage = process_xlsx(url, filename, endpoint, region, bucket_name, base_path, ak, sk, xlsx_files)
            if errorMessage is not None:
                errors.append(errorMessage)
        else:
            unknown_files.append(filename)

    return {"xlsx_files": xlsx_files, "zip_files": zip_files, "unknown_files": unknown_files, "errors": errors}
