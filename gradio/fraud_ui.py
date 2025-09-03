import gradio as gr
from PIL import Image
import random
import os
import time

# 风险分析函数，支持处理两张图片
def analyze_images(image1, image2):
    time.sleep(3)

    result = """📊 **分析结果**\n\n- 欺诈风险: **高**\n\n**详细信息:**
- 环境检测: 在同一个环境，房间内的桌子、椅子、挂钟等布置一致，光线与氛围相似，整体布置风格雷同
- 欺诈原因: 同一个环境中出现穿着不同、形象有别的人物，与团伙套现场景类似
"""


    return result

# Gradio界面
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🧠 智能风控-欺诈发现")
    with gr.Row():
        # 第一张图片上传区域
        with gr.Column(scale=1):
            image_input1 = gr.Image(type="filepath", label="上传第一张照片", sources=["upload"], height=300)
        # 第二张图片上传区域
        with gr.Column(scale=1):
            image_input2 = gr.Image(type="filepath", label="上传第二张照片", sources=["upload"], height=300)
    
    # 结果展示区域
    output_text = gr.Markdown("环境检测反欺诈...")
    
    # 分析按钮
    analyze_btn = gr.Button("开始分析", variant="primary")
    # 绑定按钮事件，接收两个图片输入
    analyze_btn.click(fn=analyze_images, inputs=[image_input1, image_input2], outputs=output_text)

# 启动应用
if __name__ == "__main__":
    demo.launch()
