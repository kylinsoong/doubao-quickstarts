from PIL import Image, ImageDraw, ImageFont
import random
import os
import time
import json

# 创建空白身份证图片的函数
def create_id_card(info):
    img = Image.new('RGB', (1000, 630), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 加载字体（需提前下载仿宋字体文件）
    font_path = "simfang.ttf"
    title_font = ImageFont.truetype(font_path, 40)
    text_font = ImageFont.truetype(font_path, 35)

    # 绘制国徽和边框（示例位置）
    draw.rectangle([(50, 50), (950, 600)], outline="black", width=3)
    draw.rectangle([(100, 100), (300, 300)], fill="gold")  # 模拟国徽区域

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

    return img

# 读取 id_infos.json 文件
with open('id_infos.json', 'r', encoding='utf-8') as f:
    id_infos = json.load(f)

# 获取当前时间戳并创建目录
timestamp = str(int(time.time()))
if not os.path.exists(timestamp):
    os.makedirs(timestamp)

# 遍历 id_infos 中的信息，生成身份证图片
for index, info in enumerate(id_infos):
    img = create_id_card(info)
    file_path = os.path.join(timestamp, f'sample_id_card_{index}.jpg')
    img.save(file_path)
    print(f"模拟身份证已生成：{file_path}")

    # 将生成的图片路径添加到 info 中
    info['image_path'] = file_path

# 更新 id_infos.json 文件
with open('id_infos.json', 'w', encoding='utf-8') as f:
    json.dump(id_infos, f, ensure_ascii=False, indent=2)

print("id_infos.json 文件已更新")
