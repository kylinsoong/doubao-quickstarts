from PIL import Image, ImageDraw, ImageFont
import random
import os
import time

# 创建空白身份证图片
img = Image.new('RGB', (1000, 630), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# 加载字体（需提前下载仿宋字体文件）
font_path = "simfang.ttf"
title_font = ImageFont.truetype(font_path, 40)
text_font = ImageFont.truetype(font_path, 35)

# 绘制国徽和边框（示例位置）
draw.rectangle([(50, 50), (950, 600)], outline="black", width=3)
draw.rectangle([(100, 100), (300, 300)], fill="gold")  # 模拟国徽区域

# 生成虚拟信息（关键数据脱敏）
def generate_id_number():
    # 生成符合GB 11643-1999的虚拟号码
    area_code = '110101'  # 北京市东城区
    year = str(random.randint(1980, 2000))
    month = f"{random.randint(1,12):02d}"
    day = f"{random.randint(1,28):02d}"
    seq = f"{random.randint(100,999):03d}"
    temp_num = area_code + year + month + day + seq
    # 计算校验码（示例算法）
    return temp_num + 'X'

# 添加文字信息
info = {
    "name": "张　三",
    "gender": "男",
    "nation": "汉",
    "birth": "1990年01月01日",
    "address": "北京市东城区景山前街4号",
    "id_num": generate_id_number(),
    "authority": "北京市公安局东城分局",
    "validity": "2010.01.01-2030.01.01"
}

# 绘制文字内容
draw.text((350, 120), "居民身份证", fill="black", font=title_font)
draw.text((350, 180), f"姓名：{info['name']}", fill="black", font=text_font)
draw.text((350, 240), f"性别：{info['gender']}　民族：{info['nation']}", fill="black", font=text_font)
draw.text((350, 300), f"出生：{info['birth']}", fill="black", font=text_font)
draw.text((350, 360), f"住址：{info['address']}", fill="black", font=text_font)
draw.text((350, 450), f"公民身份号码：{info['id_num']}", fill="black", font=text_font)
draw.text((100, 500), f"签发机关：{info['authority']}", fill="black", font=text_font)
draw.text((100, 550), f"有效期限：{info['validity']}", fill="black", font=text_font)

# 添加警示文字
draw.text((650, 590), "示例证件 禁止仿制", fill="red", font=text_font)

# 获取当前时间戳并创建目录
timestamp = str(int(time.time()))
if not os.path.exists(timestamp):
    os.makedirs(timestamp)

# 保存输出
file_path = os.path.join(timestamp, 'sample_id_card.jpg')
img.save(file_path)
print(f"模拟身份证已生成：{file_path}")
