import json
import requests
import os

from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials


collection_name = "kangfu"
project_name = "project_test_kylin"
query = "康复医疗行业的国内主流模式是什么？"

ak = os.getenv("VE_ACCESS_KEY")
sk = os.getenv("VE_SECRET_KEY")
account_id = os.getenv("VE_ACCOUNT_ID")
g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"

base_prompt = """
# 任务
你是一位文档撰写助手，你需要根据「参考资料」和「用户问题」生成一个说明性的报告，这些信息在 <context></context> XML tags 之内，你需要根据「参考资料」生成准确报告。

根据根据「参考资料」和「用户问题」生成报告要满足以下要求：
    1. 报告内容必须在参考资料范围内，根据「参考资料」准确专业回答问题，不能做任何参考资料以外的扩展解释。
    2. 报告的末尾需要注明应用的「参考资料」的文章名称，文章名称在 doc_name 字段。
    3. 如果参考资料不能找到用户问题，则回答"相关问题在知识库中不存在"。

# 任务执行
现在请你根据提供的参考资料和用户问题，遵循限制来生成报告，报告描述专业严瑾。

# 参考资料
<context>
  {}
</context>
"""

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
            "rewrite": True
        },
        "dense_weight": 0.5,
        "post_processing": {
            "get_attachment_link": True,
            "rerank_only_chunk": False,
            "rerank_switch": True,
            "chunk_group": True,
            "rerank_model": "m3-v2-rerank",
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

    return rsp.text

def is_vision_model(model_name):
    if model_name is None:
        return False
    return "vision" in model_name


def get_content_for_prompt(point: dict, image_num: int) -> str:
    content = point["content"]
    original_question = point.get("original_question")
    if original_question:
        return "当询问到相似问题时，请参考对应答案进行回答：问题：“{question}”。答案：“{answer}”".format(question=original_question, answer=content)
    if image_num > 0 and "chunk_attachment" in point and point["chunk_attachment"][0]["link"] : 
        placeholder = f"<img>图片{image_num}</img>"
        return content + placeholder
    return content


def generate_prompt(rsp_txt):
    rsp = json.loads(rsp_txt)
    if rsp["code"] != 0:
        return "", []
    prompt = ""
    image_urls = []
    rsp_data = rsp["data"]
    points = rsp_data["result_list"]
    using_vlm = is_vision_model("Doubao-1-5-pro-32k")
    image_cnt = 0

    for point in points:
        if using_vlm and "chunk_attachment" in point:
            image_link = point["chunk_attachment"][0]["link"]
            if image_link:
                image_urls.append(image_link)
                image_cnt += 1
        doc_info = point["doc_info"]
        for system_field in ["doc_name","title","chunk_title","content"] : 
            if system_field == 'doc_name' or system_field == 'title':
                if system_field in doc_info:
                    prompt += f"{system_field}: {doc_info[system_field]}\n"
            else:
                if system_field in point:
                    if system_field == "content":
                        prompt += f"content: {get_content_for_prompt(point, image_cnt)}\n"
                    else:
                        prompt += f"{system_field}: {point[system_field]}\n"
        if "table_chunk_fields" in point:
            table_chunk_fields = point["table_chunk_fields"]
            for self_field in [] : 
                find_one = next((item for item in table_chunk_fields if item["field_name"] == self_field), None)
                if find_one:
                    prompt += f"{self_field}: {find_one['field_value']}\n"

        prompt += "---\n"

    return base_prompt.format(prompt), image_urls


if __name__ == "__main__":
    rsp_txt = search_knowledge()
    prompt, image_urls = generate_prompt(rsp_txt)

    print(prompt)
    #print(len(image_urls))

