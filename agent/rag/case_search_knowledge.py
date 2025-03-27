import json
import requests
import os

from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials


collection_name = "kangfu"
project_name = "project_test_kylin"
query = "康复医疗行业的定义是什么？"
ak = os.getenv("VE_ACCESS_KEY")
sk = os.getenv("VE_SECRET_KEY")
account_id = os.getenv("VE_ACCOUNT_ID")
g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"


def prepare_request(method, path, params=None, data=None, doseq=0):
    if params:
        for key in params:
            if (isinstance(params[key], int) or isinstance(params[key], float) or isinstance(params[key], bool)):
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
        "Content-Type": "application/json; charset=utf-8",
        "Host": g_knowledge_base_domain,
        "V-Account-Id": account_id,
    }
    r.set_headers(headers)
    if params:
        r.set_query(params)
    r.set_host(g_knowledge_base_domain)
    r.set_path(path)
    if data is not None:
        r.set_body(json.dumps(data))

    # 生成签名
    credentials = Credentials(ak, sk, "air", "cn-north-1")
    SignerV4.sign(r, credentials)
    return r


def search_knowledge():
    method = "POST"
    path = "/api/knowledge/collection/search_knowledge"
    request_params = {
        "project": project_name,
        "name": collection_name,
        "query": query,
        "limit": 5,
        "pre_processing": {
            "need_instruction": True,
            "return_token_usage": True,
            "messages": [
                {
                    "role": "system",
                    "content": ""
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "rewrite": False
        },
        "dense_weight": 0.5,
        "post_processing": {
            "get_attachment_link": True,
            "rerank_only_chunk": False,
            "rerank_switch": True,
            "chunk_group": True,
            "rerank_model": "base-multilingual-rerank",
            "retrieve_count": 25,
            "chunk_diffusion_count": 5
        }
    }

    info_req = prepare_request(method=method, path=path, data=request_params)

    rsp = requests.request(
        method=info_req.method,
        url="http://{}{}".format(g_knowledge_base_domain, info_req.path),
        headers=info_req.headers,
        data=info_req.body
    )

    print(rsp.text)



if __name__ == "__main__":
    search_knowledge()
