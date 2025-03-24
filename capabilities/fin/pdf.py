from PIL import Image
import os

image_folder = "/Users/bytedance/Documents/docs/04_传统金融/海尔/images"
output_pdf = "output.pdf"

# Get all image files (JPG, PNG, etc.)
image_files = sorted(
    [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(("jpg", "jpeg", "png"))]
)

# Open images and convert them to RGB mode (for compatibility)
image_list = [Image.open(img).convert("RGB") for img in image_files]

# Save as PDF
if image_list:
    image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
    print(f"PDF saved as {output_pdf}")
else:
    print("No images found!")

