from PIL import Image

def image_format(image_path):
    with Image.open(image_path) as img:
        image_format = img.format.lower()
        if image_format not in ["jpeg", "png", "gif", "bmp", "tiff"]:
            raise ValueError(f"Unsupported image format: {image_format}")
    return image_format


format = image_format("card.png")

print(type(format))
print("card.png", image_format("card.png"))
print("make_things_happen.jpg", image_format("make_things_happen.jpg"))
