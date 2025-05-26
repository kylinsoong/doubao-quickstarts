from runtime import Args
from typings.pdf_upload.pdf_upload import Input, Output
import os
from urllib.parse import urlparse
import tos
import requests
import fitz
from io import BytesIO

def extract_filename(url):
    path = urlparse(url).path
    clean_path = path.split("~")[0].split("?")[0]
    return os.path.basename(clean_path)

def is_image(filename):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    return filename.lower().endswith(tuple(image_extensions))

def is_pdf(filename):
    image_extensions = {".pdf"}
    return filename.lower().endswith(tuple(image_extensions))

def process_image(url, filename, endpoint, region, bucket_name, base_path, ak, sk, images):
    object_key = os.path.join(base_path, filename)
    errorMessage = None
    client = tos.TosClientV2(ak, sk, endpoint, region)

    try:
        content = requests.get(url)
        client.put_object(bucket_name, object_key, content=content)
        content.close()
        target = f"https://{bucket_name}.{endpoint}/{object_key}"
        images.append(target)
    except Exception as e:
        errorMessage = 'error: {}'.format(e)

    return errorMessage

def process_pdf(url, filename, endpoint, region, bucket_name, base_path, ak, sk):
    object_key = os.path.join(base_path, filename)
    errorMessage = None
    client = tos.TosClientV2(ak, sk, endpoint, region)

    try:
        content = requests.get(url)
        client.put_object(bucket_name, object_key, content=content)
        content.close()
        target = f"https://{bucket_name}.{endpoint}/{object_key}"
        return target
    except Exception as e:
        errorMessage = 'error: {}'.format(e)

    return errorMessage

def split_pdf(pdf_tos, endpoint, region, bucket_name, base_path, ak, sk, pdfs):

    client = tos.TosClientV2(ak, sk, endpoint, region)
    errors = []

    try:
        pdf_response = requests.get(pdf_tos)
        pdf_data = pdf_response.content

        with fitz.open(stream=pdf_data, filetype="pdf") as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=300)
                img_bytes = pix.tobytes(output="png")

                original_name = os.path.splitext(extract_filename(pdf_tos))[0]
                img_name = f"{original_name}_page{page_num+1}.png"
                object_key = os.path.join(base_path, "pdf_images", img_name)

                client.put_object(
                    bucket_name,
                    object_key,
                    content=img_bytes,
                )

                img_url = f"https://{bucket_name}.{endpoint}/{object_key}"
                pdfs.append(img_url)
    except requests.RequestException as e:
        errors.append(f"PDF下载失败: {str(e)}")
    except fitz.EmptyFileError:
        errors.append("无效的PDF文件内容")
    except Exception as e:
        errors.append(f"处理异常: {str(e)}")
    return errors

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

    images = []
    pdf = ""
    pdf_tos = ""
    pdfs = []
    unknown_files = []
    errors = []

    if " " not in urls and ",http" in urls:
        url_array = urls.split(",")
    else:
        url_array = urls.split()

    for url in url_array:
        filename = extract_filename(url)
        if is_image(filename):
            errorMessage = process_image(url, filename, endpoint, region, bucket_name, base_path, ak, sk, images)
            if errorMessage is not None:
                errors.append(errorMessage)
        elif is_pdf(filename):
            pdf = filename
            results = process_pdf(url, filename, endpoint, region, bucket_name, base_path, ak, sk)
            if results is not None:
                pdf_tos = results
                pdf_errors = split_pdf(pdf_tos, endpoint, region, bucket_name, base_path, ak, sk, pdfs)
                if pdf_errors:
                    errors.extend(pdf_errors)
        else:
            unknown_files.append(filename)

    return {"pdf": pdf, "images": images, "pdf_images": pdfs, "errors": errors}
