import json 
import requests 
import logging

from volcengine.auth.SignerV4 import SignerV4 
from volcengine.base.Request import Request 
from volcengine.Credentials import Credentials 
from typing import List, Optional

# 导入配置
from config import config

# 设置日志
logger = logging.getLogger(__name__)


## 当query包含图片时，使用以下格式 
# query = [ 
#     { 
#         "text": "你的问题", 
#         "type": "text" 
#     }, 
#     { 
#         "image_url": { 
#             "url": "请传入可访问的图片URL或者Base64编码" 
#         }, 
#         "type": "image_url" 
#     } 
# ] 

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
