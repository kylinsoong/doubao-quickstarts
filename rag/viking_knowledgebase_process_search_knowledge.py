import os
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService, Collection, Doc, Point
from volcengine.viking_knowledgebase.common import Field, FieldType, IndexType, EmbddingModelType

access_key = os.environ.get("IAM_AK")
secret_key = os.environ.get("IAM_SK")
vkb_host = os.environ.get("VKB_HOST")
vkb_collection = os.environ.get("VKB_COLLECTION")
vkb_project    = os.environ.get("VKB_PROJECT")

viking_knowledgebase_service = VikingKnowledgeBaseService(host=vkb_host, scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak(access_key)
viking_knowledgebase_service.set_sk(secret_key)

query = "2024前三季新华保险银保新单期限结构趋势"

pre_processing = {
             "need_instruction": True,
             "rewrite": True,
             "messages": [
                 {
                     "role": "system",
                     "content": "你是一个智能助手。"
                 },
                 {
                     "role": "user",
                     "content": query
                 }
             ],
             "return_token_usage": True
         }

post_processing = {
             "rerank_switch": True,
             "rerank_model": "Doubao-pro-4k-rerank",
             "rerank_only_chunk": False,
            #  'chunk_diffusion_count': 2,
             "retrieve_count": 10,
            #  "endpoint_id": "ep-20240725211310-b28mr",
             "chunk_group": True,
             "get_attachment_link": True
         }

res = viking_knowledgebase_service.search_knowledge(collection_name=vkb_collection,project=vkb_project,query=query,limit=5,pre_processing=pre_processing,post_processing=post_processing)

for r in res['result_list']:
    print(r['content'])


