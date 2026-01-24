#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将PDF文件的每一页转换为一张图片
优化版本：增加了性能、功能和用户体验
"""

import os
import argparse
import logging
from typing import List, Optional
from pdf2image import convert_from_path
from PIL import Image
from tqdm import tqdm

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def pdf_to_images(
    pdf_path: str,
    output_folder: Optional[str] = None,
    dpi: int = 300,
    fmt: str = 'PNG',
    quality: int = 95,
    first_page: Optional[int] = None,
    last_page: Optional[int] = None,
    thread_count: int = 1
) -> List[str]:
    """
    将PDF文件转换为图片
    
    Args:
        pdf_path (str): PDF文件路径
        output_folder (str, optional): 输出图片的文件夹路径
        dpi (int, optional): 图片分辨率，默认300
        fmt (str, optional): 图片格式，默认PNG
        quality (int, optional): 图片质量（0-100），仅对JPEG等有损格式有效
        first_page (int, optional): 开始转换的页码（从1开始）
        last_page (int, optional): 结束转换的页码（从1开始）
        thread_count (int, optional): 转换时使用的线程数
        
    Returns:
        list: 生成的图片文件路径列表
    """
    # 参数验证
    if not pdf_path:
        raise ValueError("PDF路径不能为空")
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    if not os.path.isfile(pdf_path):
        raise IsADirectoryError(f"{pdf_path} 是目录，不是文件")
    
    if not pdf_path.lower().endswith('.pdf'):
        logger.warning(f"文件扩展名不是.pdf，可能不是有效的PDF文件: {pdf_path}")
    
    if dpi <= 0:
        raise ValueError("DPI必须大于0")
    
    if quality < 0 or quality > 100:
        raise ValueError("图片质量必须在0-100之间")
    
    supported_formats = ['PNG', 'JPEG', 'JPG', 'BMP', 'TIFF', 'TIF']
    fmt = fmt.upper()
    if fmt not in supported_formats:
        raise ValueError(f"不支持的图片格式: {fmt}，支持的格式有: {', '.join(supported_formats)}")
    
    # 处理输出文件夹
    if output_folder is None:
        output_folder = os.path.dirname(pdf_path)
    
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取PDF文件名（不包含扩展名）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    try:
        logger.info(f"开始转换PDF: {pdf_path}")
        logger.info(f"输出目录: {output_folder}")
        logger.info(f"参数: DPI={dpi}, 格式={fmt}, 质量={quality}, 线程数={thread_count}")
        
        # 将PDF转换为图片
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            use_cropbox=True,  # 使用裁剪框确保正确的页面边界
            first_page=first_page,
            last_page=last_page,
            thread_count=thread_count,
            fmt=fmt.lower(),  # 让pdf2image直接使用正确的格式
            output_folder=None  # 不使用内部输出，手动处理保存
        )
        
        image_paths = []
        logger.info(f"共需转换 {len(images)} 页")
        
        # 保存图片，使用进度条
        for i, image in enumerate(tqdm(images, desc="转换进度")):
            # 计算实际页码（考虑first_page）
            actual_page = i + 1 if first_page is None else i + first_page
            
            # 生成图片文件名，确保页码格式统一（如001, 002）
            image_filename = f"{pdf_name}_page_{actual_page:03d}.{fmt.lower()}"
            image_path = os.path.join(output_folder, image_filename)
            
            # 根据格式设置保存参数
            save_kwargs = {}
            if fmt in ['JPEG', 'JPG']:
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True  # 启用优化
            elif fmt == 'PNG':
                save_kwargs['optimize'] = True
                save_kwargs['compress_level'] = 9  # PNG最大压缩级别
            
            # 保存图片
            image.save(image_path, fmt, **save_kwargs)
            image_paths.append(image_path)
            
        logger.info(f"转换完成！共生成 {len(image_paths)} 张图片")
        return image_paths
        
    except Exception as e:
        logger.error(f"转换失败: {e}")
        raise


def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="将PDF文件的每一页转换为图片")
    parser.add_argument("pdf_path", help="PDF文件路径")
    parser.add_argument("-o", "--output", help="输出图片的文件夹路径")
    parser.add_argument("-d", "--dpi", type=int, default=300, help="图片分辨率")
    parser.add_argument("-f", "--format", choices=['PNG', 'JPEG', 'JPG', 'BMP', 'TIFF', 'TIF'], 
                        default='PNG', help="图片格式")
    parser.add_argument("-q", "--quality", type=int, default=95, 
                        help="图片质量（0-100），仅对JPEG等有损格式有效")
    parser.add_argument("-s", "--start", type=int, help="开始转换的页码")
    parser.add_argument("-e", "--end", type=int, help="结束转换的页码")
    parser.add_argument("-t", "--threads", type=int, default=1, 
                        help="转换时使用的线程数")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细日志")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_arguments()
        
        # 设置日志级别
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        
        # 调用转换函数
        generated_images = pdf_to_images(
            pdf_path=args.pdf_path,
            output_folder=args.output,
            dpi=args.dpi,
            fmt=args.format,
            quality=args.quality,
            first_page=args.start,
            last_page=args.end,
            thread_count=args.threads
        )
        
        print(f"\n转换完成！共生成 {len(generated_images)} 张图片")
        if args.output:
            print(f"图片保存路径: {args.output}")
        else:
            print(f"图片保存路径: {os.path.dirname(args.pdf_path)}")
            
    except KeyboardInterrupt:
        print("\n用户中断了转换过程")
        exit(1)
    except Exception as e:
        print(f"转换过程中发生错误: {e}")
        exit(1)