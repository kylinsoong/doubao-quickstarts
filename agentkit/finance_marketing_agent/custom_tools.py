import json 
import requests 

from volcengine.auth.SignerV4 import SignerV4 
from volcengine.base.Request import Request 
from volcengine.Credentials import Credentials 
import os 
from typing import List

#account_id = "your accountid" 

g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com" 
apikey = os.getenv("VIKING_SERVICE_API_KEY") 
service_resource_id = os.getenv("VIKING_SERVICE_RESOURCE_ID") 


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
    r.set_connection_timeout(10) 
    r.set_socket_timeout(10) 
    headers = { 
        "Accept": "application/json", 
        "Content-Type": "application/json;charset=UTF-8", 
        "Host": g_knowledge_base_domain, 
        'Authorization': f'Bearer {apikey}' 
    } 
    r.set_headers(headers) 
    if params: 
        r.set_query(params) 
    r.set_host(g_knowledge_base_domain) 
    r.set_path(path) 
    if data is not None: 
        r.set_body(json.dumps(data)) 
    return r 


def knowledge_service_search(query: str = None) -> List[str]: 
    """
    知识服务搜索工具，用于从知识服务中检索相关信息并返回图片链接。
    
    参数:
    query: 搜索查询词
    
    返回:
    List[str]: 包含图片链接的列表
    """
    # 如果没有提供参数，使用默认值
    
    if query is None:
        raise ValueError("query is not provided")
    
    method = "POST" 
    path = "/api/knowledge/service/chat" 
    request_params = { 
    "service_resource_id": service_resource_id, 
    "messages":[
        { 
            "role": "user", 
            "content":query 
        } 
    ], 
    "stream": False 
    } 

    info_req = prepare_request(method=method, path=path, data=request_params) 
    rsp = requests.request( 
        method=info_req.method, 
        url="http://{}{}".format(g_knowledge_base_domain, info_req.path), 
        headers=info_req.headers, 
        data=info_req.body 
    ) 
    rsp.encoding = "utf-8" 
    
    # Parse response and extract image links 
    image_links = [] 
    try: 
        response_data = json.loads(rsp.text) 
        # Check if response contains image links 
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
        # Also check for image links in other possible response fields 
        if "images" in response_data: 
            for image in response_data["images"]: 
                if "url" in image: 
                    image_links.append(image["url"]) 
    except json.JSONDecodeError: 
        print("Failed to parse response as JSON") 
    return image_links
