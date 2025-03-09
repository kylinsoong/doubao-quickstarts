import requests
import filetype


def fileType(url):
    response = requests.get(url, stream=True)
    file_name = "downloaded_file"
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    kind = filetype.guess(file_name)
    if kind:
        return kind.mime, kind.extension
    else:
        return None, None


url_1 = "https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/2ebdd41186704446b3c9b4c076c8f36e.zip~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743918961&x-signature=eBbutSO1bHBBkXqoDmBtLgmSwrw%3D"

url_2 = "https://p3-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/13d5426d01904b54b52868db0c23a858.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743918483&x-signature=IQvEQ21pjrr4%2FBT%2FqMKI0KNNyVI%3D"

type = fileType(url_2)

print(type)
