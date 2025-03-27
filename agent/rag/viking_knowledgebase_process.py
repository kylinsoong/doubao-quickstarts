import os
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService, Collection, Doc, Point
from volcengine.viking_knowledgebase.common import Field, FieldType, IndexType, EmbddingModelType

access_key = os.environ.get("IAM_AK")
secret_key = os.environ.get("IAM_SK")
vkb_host = os.environ.get("VKB_HOST")
vkb_collection = os.environ.get("VKB_COLLECTION")
vkb_project    = os.environ.get("VKB_PROJECT")
model = os.environ.get("ARK_EP_ID")

viking_knowledgebase_service = VikingKnowledgeBaseService(host=vkb_host, scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak(access_key)
viking_knowledgebase_service.set_sk(secret_key)

collection = viking_knowledgebase_service.get_collection(collection_name=vkb_collection,project=vkb_project)

print(collection.collection_name)
print(collection.description)
print(collection.doc_num)
print(collection.create_time)
print(collection.update_time)
print(collection.creator)
print(collection.pipeline_list)
print(collection.preprocessing)
print(collection.fields)
print(collection.project)
print(collection.resource_id)


collections = viking_knowledgebase_service.list_collections(project=vkb_project)

for collection in collections:
   print(collection.collection_name, collection.doc_num, collection.create_time, collection.update_time, collection.creator, collection.resource_id)



query = "2024前三季新华保险银保新单期限结构趋势"

points = viking_knowledgebase_service.search_collection(collection_name=vkb_collection,project=vkb_project,query=query,limit=5)

for point in points:
    print(point.chunk_title)

for point in points:
    print(point.original_question, point.process_time, point.rerank_score, point.score, point.chunk_id)

for point in points:
    print(point.content)
    print("------------------")




results = viking_knowledgebase_service.search_and_generate(collection_name=vkb_collection,project=vkb_project,query=query)

print(results['collection_name'])
print(results['count'])
print(results['generated_answer'])
print(results['prompt'])
print()
print(results['usage'])



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



model = model
m_messages = [{
    "role": "system",
    "content": "你是一个智能助手。"
    },
    {
        "role": "user",
        "content": query
    }
]


res = viking_knowledgebase_service.chat_completion(model=model, messages=m_messages, max_tokens=4096, temperature=0.1)

print(res['generated_answer'])
print()
print(res['usage'])
