from urllib.parse import urlparse

def extract_filename(url):
    parsed_url = urlparse(url)
    path = parsed_url.path 
    filename = path.split("/")[-1].split("~")[0]
    return filename


url_1 = "https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/2ebdd41186704446b3c9b4c076c8f36e.zip~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743918961&x-signature=eBbutSO1bHBBkXqoDmBtLgmSwrw%3D"

url_2 = "https://p3-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/13d5426d01904b54b52868db0c23a858.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743918483&x-signature=IQvEQ21pjrr4%2FBT%2FqMKI0KNNyVI%3D"


print(extract_filename(url_1))

print(extract_filename(url_2))
