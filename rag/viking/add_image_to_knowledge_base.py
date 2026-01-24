#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量数据库VikingDB添加图片到知识库示例

使用说明：
1. 确保已安装必要的库：pip install requests volcengine
2. 设置环境变量：
   - VOLCENGINE_ACCESS_KEY: 您的Access Key
   - VOLCENGINE_SECRET_KEY: 您的Secret Key
   - IMAGE_URL: 图片的URL地址
3. 运行脚本：python add_image_to_knowledge_base.py
"""

import json
import os

# 配置信息 - 从环境变量读取
AK = os.environ.get("VOLCENGINE_ACCESS_KEY")  # 从环境变量读取Access Key
SK = os.environ.get("VOLCENGINE_SECRET_KEY")  # 从环境变量读取Secret Key
REGION = "cn-beijing"  # 地域

# 知识库和图片信息
KB_NAME = "images"  # 知识库名称
IMAGE_URL = os.environ.get("IMAGE_URL")  # 从环境变量读取图片URL
DOC_ID = "image_1"  # 文档ID，需唯一
DOC_NAME = "Example_Image"  # 文档名称
DOC_TYPE = "png"  # 文档类型

# 检查环境变量是否设置
if not AK:
    raise ValueError("请设置环境变量 VOLCENGINE_ACCESS_KEY")
if not SK:
    raise ValueError("请设置环境变量 VOLCENGINE_SECRET_KEY")
if not IMAGE_URL:
    raise ValueError("请设置环境变量 IMAGE_URL")

# 使用viking_knowledgebase模块发送请求
try:
    from volcengine.viking_knowledgebase.VikingKnowledgeBaseService import VikingKnowledgeBaseService
    
    # 创建服务实例
    service = VikingKnowledgeBaseService(
        host="api-knowledgebase.mlp.cn-beijing.volces.com",
        region=REGION,
        ak=AK,
        sk=SK,
        scheme="https"
    )
    
    # 构建请求参数
    params = {
        "collection_name": KB_NAME,
        "add_type": "url",
        "doc_id": DOC_ID,
        "doc_name": DOC_NAME,
        "doc_type": DOC_TYPE,
        "url": IMAGE_URL
    }
    
    # 使用json方法发送请求，api参数为"AddDoc"
    # 将params转换为JSON字符串
    import json as json_module
    response = service.json("AddDoc", {}, json_module.dumps(params))
    
    print("\n使用viking_knowledgebase模块的响应:")
    print(f"响应内容: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
except ImportError as e:
    print(f"\n导入模块错误: {str(e)}")
    print("请确保已安装volcengine库: pip install volcengine")

except Exception as e:
    print(f"\n发生错误: {str(e)}")
    import traceback
    traceback.print_exc()
