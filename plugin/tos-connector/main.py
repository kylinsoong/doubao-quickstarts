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


def process_xlsx(url, filename, endpoint, region, bucket_name, base_path, ak, sk):
    object_key = os.path.join(base_path, filename)
    errorMessage = None
    client = tos.TosClientV2(ak, sk, endpoint, region)
    
    try:
        content = requests.get(url)
        client.put_object(bucket_name, object_key, content=content)
        content.close()
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
                        xlsx_files.append(file)
                    else:
                        unknown_files.append(file)
                    
        except Exception as e:
            errorMessage = f'Error processing ZIP {filename}: {e}'

    return errorMessage    



def handler(urls, endpoint, region, bucket_name, base_path, ak, sk):
    url_array = urls.split()
    zip_files = []
    xlsx_files = []
    unknown_files = []
    for url in url_array:
        filename = extract_filename(url)
        if filename.endswith(".zip"):
            process_zip(url, filename, xlsx_files, unknown_files, endpoint, region, bucket_name, base_path, ak, sk)
            zip_files.append(filename)
        elif filename.endswith(".xlsx"):
            process_xlsx(url, filename, endpoint, region, bucket_name, base_path, ak, sk)
            xlsx_files.append(filename)
        else:
            unknown_files.append(filename)

    print(zip_files, xlsx_files, unknown_files)


url_1 = "https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/2ebdd41186704446b3c9b4c076c8f36e.zip~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743918961&x-signature=eBbutSO1bHBBkXqoDmBtLgmSwrw%3D https://p3-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/13d5426d01904b54b52868db0c23a858.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743918483&x-signature=IQvEQ21pjrr4%2FBT%2FqMKI0KNNyVI%3D https://p3-bot-sign.byteimg.com/test.xlsx"

ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
endpoint = os.getenv('TOS_ENDPOINT')
region = os.getenv('TOS_REGION')
bucket_name = os.getenv('TOS_BUCKET')

handler(url_1, endpoint, region, bucket_name, "9836", ak, sk)
