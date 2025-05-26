


urls = "https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/f55d2ddd99404397b8504e823beea49d.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743951823&x-signature=qa93V8UTS87oYAZs4ih%2B2AOmfNI%3D,https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/d043ab9340c143b69d008a01e1f87759.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743951823&x-signature=vrDz0h3r8Cs7gTDZhLSaZbJuA4M%3D,https://p6-bot-sign.byteimg.com/tos-cn-i-v4nquku3lp/d642230c48f44e98b5a79d955809ae29.xlsx~tplv-v4nquku3lp-image.image?rk3s=68e6b6b5&x-expires=1743951823&x-signature=iwRO8PE0R2VFG3UxiX57R4SSas0%3D"

if " " not in urls and ",http" in urls:
    url_array = urls.split(",")
    print(url_array)
else:
    url_array = urls.split()
