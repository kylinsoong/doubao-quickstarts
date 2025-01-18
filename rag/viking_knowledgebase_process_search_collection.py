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

points = viking_knowledgebase_service.search_collection(collection_name=vkb_collection,project=vkb_project,query=query,limit=5)

for point in points:
    print(point.chunk_title)

for point in points:
    print(point.original_question, point.process_time, point.rerank_score, point.score, point.chunk_id)

for point in points:
    print(point.content)
    print("------------------")
