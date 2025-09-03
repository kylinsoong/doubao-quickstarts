import gradio as gr
from PIL import Image
import random
import os
import time

# Dummy risk analysis function
def analyze_image(image):
    if image is None:
        return "请上传一张照片进行分析"
    
    file_name = os.path.basename(image)

    time.sleep(1)

    if file_name == "1001.jpeg":
        result = """📊 **分析结果**\n\n- 风险等级: **低风险**\n\n**详细信息:**
- 性别: 女
- 年龄: 30-35
- 职业: 白领
- 表情: 平静
- 背景: 室内办公环境，背景有‘Bytedance’标志，可能是字节跳动公司办公场所
- 戴眼镜: 否
- 脸部遮挡: 否
- 戴耳机: 否
- 戴口罩: 否
- 异常: 无
"""
        return result
    elif file_name == "1195.jpeg":
        result = """📊 **分析结果**\n\n- 风险等级: **高风险**\n\n**详细信息:**
- 性别: 男
- 年龄: 50-55
- 职业: 无特定职业
- 表情: 惊讶
- 背景: 医院
- 戴眼镜: 否
- 脸部遮挡: 否
- 戴耳机: 否
- 戴口罩: 否
- 异常: 纹身
"""
        return result
    else:
        risk_levels = ["低风险", "中风险", "高风险"]
        reasons = [
            "图像质量较低，无法识别关键信息。",
            "检测到异常行为，请进一步人工审核。",
            "数据完全符合要求，暂无风险。",
            "存在高风险特征，请立即跟进处理。"
        ]
    
        risk = random.choice(risk_levels)
        reason = random.choice(reasons)
    
        return f"📊 **分析结果**\n\n- 风险等级: **{risk}**\n- 说明: {reason}"

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🧠 智能风控-视觉风控")
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="filepath", label="上传照片", sources=["upload"], height=300)
        with gr.Column(scale=2):
            output_text = gr.Markdown("贷前核身实时风险评估...")

    analyze_btn = gr.Button("开始核身", variant="primary")
    analyze_btn.click(fn=analyze_image, inputs=image_input, outputs=output_text)

# Launch
if __name__ == "__main__":
    demo.launch()

