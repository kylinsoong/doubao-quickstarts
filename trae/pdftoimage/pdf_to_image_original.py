#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将PDF文件的每一页转换为一张图片
"""

import os
from pdf2image import convert_from_path
from PIL import Image

def pdf_to_images(pdf_path, output_folder=None, dpi=300, fmt='PNG'):
    """
    将PDF文件转换为图片
    
    Args:
        pdf_path (str): PDF文件路径
        output_folder (str, optional): 输出图片的文件夹路径
        dpi (int, optional): 图片分辨率，默认300
        fmt (str, optional): 图片格式，默认PNG
        
    Returns:
        list: 生成的图片文件路径列表
    """
    # 检查PDF文件是否存在
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    # 如果未指定输出文件夹，使用PDF文件所在目录
    if output_folder is None:
        output_folder = os.path.dirname(pdf_path)
    
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取PDF文件名（不包含扩展名）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    try:
        # 将PDF转换为图片，确保每页单独转换
        images = convert_from_path(
            pdf_path, 
            dpi=dpi, 
            use_cropbox=True,  # 使用裁剪框确保正确的页面边界
            single_file=False,  # 确保每页生成一个文件
            output_folder=None  # 不使用内部输出，手动处理保存
        )
        
        image_paths = []
        for i, image in enumerate(images):
            # 生成图片文件名
            image_filename = f"{pdf_name}_page_{i+1}.{fmt.lower()}"
            image_path = os.path.join(output_folder, image_filename)
            
            # 保存图片
            image.save(image_path, fmt)
            image_paths.append(image_path)
            print(f"已生成图片: {image_path}")
        
        return image_paths
        
    except Exception as e:
        print(f"转换失败: {e}")
        raise

if __name__ == "__main__":
    # 设置PDF文件路径
    pdf_file_path = "/Users/bytedance/Downloads/0103.pdf"
    
    # 设置输出文件夹
    output_dir = os.path.join(os.path.dirname(__file__), "output_images_03")
    
    try:
        print(f"开始转换PDF: {pdf_file_path}")
        generated_images = pdf_to_images(pdf_file_path, output_dir)
        print(f"\n转换完成！共生成 {len(generated_images)} 张图片")
        print(f"图片保存路径: {output_dir}")
    except Exception as e:
        print(f"转换过程中发生错误: {e}")
        exit(1)