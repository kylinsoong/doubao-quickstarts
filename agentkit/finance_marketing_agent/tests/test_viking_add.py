import json 
import requests 
import logging
import os
import sys

from volcengine.auth.SignerV4 import SignerV4 
from volcengine.base.Request import Request 
from volcengine.Credentials import Credentials 
from typing import List, Optional

# 添加上级目录到 Python 路径，以便导入 config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入配置
from config import config

# 设置日志
logger = logging.getLogger(__name__)


def prepare_request(method, path, params=None, data=None, doseq=0): 
    """准备请求对象"""
    if params: 
        for key in params: 
            if ( 
                    isinstance(params[key], int) 
                    or isinstance(params[key], float) 
                    or isinstance(params[key], bool) 
            ): 
                params[key] = str(params[key]) 
            elif isinstance(params[key], list): 
                if not doseq: 
                    params[key] = ",".join(params[key]) 
    
    r = Request() 
    r.set_shema("http") 
    r.set_method(method) 
    r.set_connection_timeout(config.knowledge_service.timeout) 
    r.set_socket_timeout(config.knowledge_service.timeout) 
    
    headers = { 
        "Accept": "application/json", 
        "Content-Type": "application/json;charset=UTF-8", 
        "Host": config.knowledge_service.domain, 
        'Authorization': f'Bearer {config.knowledge_service.api_key}' 
    } 
    
    r.set_headers(headers) 
    if params: 
        r.set_query(params) 
    r.set_host(config.knowledge_service.domain) 
    r.set_path(path) 
    if data is not None: 
        r.set_body(json.dumps(data)) 
    
    return r 


def knowledge_service_search(query: str, service_resource_id: Optional[str] = None) -> List[str]: 
    """
    知识服务搜索工具，用于从知识服务中检索相关信息并返回图片链接。
    
    参数:
    query: 搜索查询词
    service_resource_id: 知识服务资源ID（可选，默认使用配置中的值）
    
    返回:
    List[str]: 包含图片链接的列表
    """
    # 参数验证
    if not query: 
        logger.error("查询参数不能为空")
        raise ValueError("query is required") 
    
    # 使用默认资源ID（如果未提供）
    resource_id = service_resource_id or config.knowledge_service.resource_id
    if not resource_id: 
        logger.error("知识服务资源ID不能为空")
        raise ValueError("service_resource_id is required") 
    
    try: 
        method = "POST" 
        path = "/api/knowledge/service/chat" 
        
        request_params = { 
            "service_resource_id": resource_id, 
            "messages":[
                { 
                    "role": "user", 
                    "content": query 
                } 
            ], 
            "stream": False 
        }

        # 准备请求
        info_req = prepare_request(method=method, path=path, data=request_params) 
        
        # 发送请求
        logger.info(f"发送知识服务请求，查询: {query[:50]}...")
        rsp = requests.request( 
            method=info_req.method, 
            url=f"http://{config.knowledge_service.domain}{info_req.path}", 
            headers=info_req.headers, 
            data=info_req.body, 
            timeout=config.knowledge_service.timeout 
        ) 
        
        rsp.encoding = "utf-8" 
        rsp.raise_for_status()  # 检查HTTP错误
        
        # 解析响应并提取图片链接 
        response_data = rsp.json()
        image_links = [] 
        
        # 检查响应结构
        if "data" in response_data: 
            data = response_data["data"] 
            if "result_list" in data: 
                result_list = data["result_list"] 
                for result in result_list: 
                    if "chunk_attachment" in result: 
                        for attachment in result["chunk_attachment"]: 
                            if attachment.get("type") == "doc-image" and "link" in attachment: 
                                image_url = attachment["link"] 
                                if image_url: 
                                    image_links.append(image_url) 
        # 检查其他可能的图片链接字段 
        if "images" in response_data: 
            for image in response_data["images"]: 
                if "url" in image: 
                    image_links.append(image["url"])
        
        logger.info(f"知识服务请求成功，找到 {len(image_links)} 个图片链接")
        return image_links 
        
    except requests.exceptions.RequestException as e: 
        logger.error(f"知识服务请求失败: {str(e)}")
        return []
    except json.JSONDecodeError: 
        logger.error(f"解析知识服务响应失败: {rsp.text[:100]}...")
        return []
    except Exception as e: 
        logger.error(f"知识服务搜索发生未知错误: {str(e)}")
        return []


def knowledge_service_add_file(url: str, service_resource_id: Optional[str] = None) -> dict:
    """
    知识服务添加文件工具，用于通过URL方式向知识库添加文件。
    
    参数:
    url: 待上传的文件URL链接（必填）
    service_resource_id: 知识服务资源ID（可选，默认使用配置中的值）
    
    返回:
    dict: 包含操作结果的字典
    """
    import os
    import hashlib
    import datetime
    
    # 参数验证
    if not url:
        logger.error("URL参数不能为空")
        raise ValueError("url is required")
    
    # 使用默认资源ID（如果未提供）
    resource_id = service_resource_id or config.knowledge_service.resource_id
   # print(resource_id, os.getenv("VIKING_SERVICE_RESOURCE_ID", ""))
    logger.info(f"当前资源ID配置: {resource_id}")
    if not resource_id:
        logger.error("知识服务资源ID不能为空")
        logger.error("请设置环境变量 VIKING_SERVICE_RESOURCE_ID 或在调用时提供 service_resource_id 参数")
        raise ValueError("service_resource_id is required or must be configured")
    
    try:
        
        # 从URL自动生成必要参数
        # 提取文件名作为doc_name
        doc_name = os.path.basename(url)
        
        # 从文件名提取文件类型（扩展名）作为doc_type
        doc_type = os.path.splitext(doc_name)[1].lower().lstrip('.')
        if not doc_type:
            doc_type = "txt"  # 默认类型
        
        # 生成唯一的doc_id（基于URL和时间戳的哈希值）
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        doc_id = hashlib.md5(f"{url}_{timestamp}".encode()).hexdigest()
        
        method = "POST"
        path = "/api/knowledge/doc/add"
        
        # 构建请求参数
        request_params = {
            "collection_name": "images",
            "add_type": "url",  # 固定为url方式
            "url": url
        }
        
        
        # 准备请求
        info_req = prepare_request(method=method, path=path, data=request_params)
        
        # 发送请求
        logger.info(f"发送知识服务添加文件请求，URL: {url}, doc_name: {doc_name}")
        rsp = requests.request(
            method=info_req.method,
            url=f"http://{config.knowledge_service.domain}{info_req.path}",
            headers=info_req.headers,
            data=info_req.body,
            timeout=config.knowledge_service.timeout
        )
        
        rsp.encoding = "utf-8"
        rsp.raise_for_status()  # 检查HTTP错误
        
        # 解析响应
        response_data = rsp.json()
        logger.info(f"知识服务添加文件请求成功: {response_data}")
        return response_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"知识服务添加文件请求失败: {str(e)}")
        raise
    except json.JSONDecodeError:
        logger.error(f"解析知识服务添加文件响应失败: {rsp.text[:100]}...")
        raise
    except Exception as e:
        logger.error(f"知识服务添加文件发生未知错误: {str(e)}")
        raise

if __name__ == "__main__":
    # 演示：通过 URL 向知识服务添加文件
    demo_url = "https://ts1.tc.mm.bing.net/th/id/OIP-C.oLnKOfLPRGzydgYJmqFXjgHaCZ?rs=1&pid=ImgDetMain&o=7&rm=3"
    try:
        result = knowledge_service_add_file(url=demo_url)
        print("添加文件成功，返回结果：", result)
    except Exception as e:
        print("添加文件失败：", e)


