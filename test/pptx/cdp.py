from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Initialize presentation
prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
content_slide_layout = prs.slide_layouts[1]

# Title Slide
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "产品对比分析汇报"
subtitle.text = "DataFinder vs DataLeap vs VeCDP"

# Helper function to add slide with title and content
def add_content_slide(prs, title_text, content_text):
    slide = prs.slides.add_slide(content_slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    title.text = title_text
    content.text = content_text

# Content slides
slides_content = [
    ("一、产品定位对比",
     "DataFinder：增长分析平台，聚焦营销增长；\n"
     "DataLeap：数智平台，统一数据底座；\n"
     "VeCDP：客户数据平台，专注用户精细化运营"),
    
    ("二、目标用户与使用场景",
     "DataFinder：增长团队，场景如投放、留存分析；\n"
     "DataLeap：数据开发、治理全链条；\n"
     "VeCDP：市场营销，支持用户旅程、私域触达"),
    
    ("三、核心能力对比",
     "- DataFinder：多维分析，A/B测试，偏业务端\n"
     "- DataLeap：支持湖仓一体，强数据治理\n"
     "- VeCDP：用户标签、旅程自动化、Lookalike营销"),
    
    ("四、产品优势与亮点",
     "DataFinder：上手快，适用于快速验证场景；\n"
     "DataLeap：支撑大型数据治理，模块丰富；\n"
     "VeCDP：运营自动化，联动广告平台，闭环营销"),
    
    ("五、适用场景建议",
     "- DataFinder：快速部署增长分析\n"
     "- DataLeap：构建数据中台\n"
     "- VeCDP：提升转化率与精细运营")
]

# Add content slides
for title_text, content_text in slides_content:
    add_content_slide(prs, title_text, content_text)

# Save presentation
pptx_path = "CDP_Comparison.pptx"
prs.save(pptx_path)

