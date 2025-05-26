import fitz  # PyMuPDF
import requests
from pathlib import Path

pdf_url = "https://pub-kylin.tos-cn-beijing.volces.com/9036/e9d7ee6e3d604914bdfe681dbae89299.pdf"
response = requests.get(pdf_url)
pdf_data = response.content

output_dir = Path("pdf_images")
output_dir.mkdir(exist_ok=True)

doc = fitz.open(stream=pdf_data, filetype="pdf")

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=300)  # 设置300 DPI分辨率
    img_path = output_dir / f"page_{page_num + 1}.png"
    pix.save(img_path)
    print(f"已保存: {img_path}")

print(f"转换完成！共转换 {len(doc)} 页")
