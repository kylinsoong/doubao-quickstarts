
import json
import requests

from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials

collection_name = "investune_docs"
project_name = "project_test_kylin"
query = "DLSP: A Document Level Structure Parser for Multi-Page Digital Documents 这篇论文是关于什么的"
ak = "your ak"
sk = "your sk"
account_id = "your account_id"
g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"

base_prompt = """# 任务
你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内，你需要根据参考资料给出准确，简洁的回答。

你的回答要满足以下要求：
    1. 回答内容必须在参考资料范围内，尽可能简洁地回答问题，不能做任何参考资料以外的扩展解释。
    2. 回答中需要根据客户问题和参考资料保持与客户的友好沟通。
    3. 如果参考资料不能帮助你回答用户问题，告知客户无法回答该问题，并引导客户提供更加详细的信息。
    4. 为了保密需要，委婉地拒绝回答有关参考资料的文档名称或文档作者等问题。

# 任务执行
现在请你根据提供的参考资料，遵循限制来回答用户的问题，你的回答需要准确和完整。

# 参考资料
<context>
  {}
</context>
"""

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
    "project": "project_test_kylin",
    "name": "investune_docs",
    "query": "DLSP: A Document Level Structure Parser for Multi-Page Digital Documents 这篇论文是关于什么的",
    "limit": 10,
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
                "content": "DLSP: A Document Level Structure Parser for Multi-Page Digital Documents 这篇论文是关于什么的"
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
    # print("search res = {}".format(rsp.text))
    return rsp.text

def chat_completion(message, stream=False, return_token_usage=True, temperature=0.7, max_tokens=4096):
    method = "POST"
    path = "/api/knowledge/chat/completions"
    request_params = {
        "messages": message,
        "stream": True,
        "return_token_usage": True,
        "model": "Doubao-pro-32k",
        "max_tokens": 4096,
        "temperature": 0.7,
        "model_version": "241215"
    }

    info_req = prepare_request(method=method, path=path, data=request_params)
    rsp = requests.request(
        method=info_req.method,
        url="http://{}{}".format(g_knowledge_base_domain, info_req.path),
        headers=info_req.headers,
        data=info_req.body
    )
    rsp.encoding = "utf-8"
    print("chat completion res = {}".format(rsp.text))

def is_vision_model(model_name):
    if model_name is None:
        return False
    return "vision" in model_name
def get_content_for_prompt(point: dict, image_num: int) -> str:
    content = point["content"]
    original_question = point.get("original_question")
    if original_question:
        # faq 召回场景，content 只包含答案，需要把原问题也拼上
        return "当询问到相似问题时，请参考对应答案进行回答：问题：“{question}”。答案：“{answer}”".format(
                question=original_question, answer=content)
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
    using_vlm = is_vision_model("Doubao-pro-32k")
    image_cnt = 0

    for point in points:
        # 提取图片链接
        if using_vlm and "chunk_attachment" in point:
            image_link = point["chunk_attachment"][0]["link"]
            if image_link:
                image_urls.append(image_link)
                image_cnt += 1
        # 先拼接系统字段
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
                # 使用 next() 从 table_chunk_fields 中找到第一个符合条件的项目
                find_one = next((item for item in table_chunk_fields if item["field_name"] == self_field), None)
                if find_one:
                    prompt += f"{self_field}: {find_one['field_value']}\n"

        prompt += "---\n"

    return base_prompt.format(prompt), image_urls


def search_knowledge_and_chat_completion():
    # 1.执行search_knowledge
    rsp_txt = search_knowledge()
    # 2.生成prompt
    prompt, image_urls = generate_prompt(rsp_txt)
    # todo:用户需要本地缓存对话信息，并按照顺序依次加入到messages中
    # 3.拼接message对话, 问题对应role为user，系统对应role为system, 答案对应role为assistant, 内容对应content
    if image_urls:
          multi_modal_msg = [{"type": "text", "text": query}]
          for image_url in image_urls:
              multi_modal_msg.append({"type": "image_url", "image_url": {"url": image_url}})
          messages =[
              {
                  "role": "system",
                  "content": prompt
              },
              {
                  "role": "user",
                  "content": multi_modal_msg
              }
          ]
    else:
        messages =[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": query
            }
        ]

    # 4.调用chat_completion
    chat_completion(messages)

if __name__ == "__main__":
    search_knowledge_and_chat_completion()

