#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量数据库VikingDB添加图片到知识库示例

使用说明：
1. 确保已安装必要的库：pip install requests volcengine
2. 替换AK和SK为您的实际访问密钥
3. 运行脚本：python add_image_to_knowledge_base.py
"""

import json

# 配置信息 - 请根据实际情况修改
AK = ""  # 替换为您的Access Key
SK = ""  # 替换为您的Secret Key
REGION = "cn-beijing"  # 地域

# 知识库和图片信息
KB_NAME = "images"  # 知识库名称
IMAGE_URL = ""
DOC_ID = "image_1"  # 文档ID，需唯一
DOC_NAME = "Example_Image"  # 文档名称
DOC_TYPE = "png"  # 文档类型

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
