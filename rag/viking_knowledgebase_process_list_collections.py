import os
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService, Collection, Doc, Point
from volcengine.viking_knowledgebase.common import Field, FieldType, IndexType, EmbddingModelType

access_key = os.environ.get("IAM_AK")
secret_key = os.environ.get("IAM_SK")
vkb_host = os.environ.get("VKB_HOST")
vkb_project    = os.environ.get("VKB_PROJECT")

viking_knowledgebase_service = VikingKnowledgeBaseService(host=vkb_host, scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak(access_key)
viking_knowledgebase_service.set_sk(secret_key)

collections = viking_knowledgebase_service.list_collections(project=vkb_project)

for collection in collections:
   print(collection.collection_name, collection.doc_num, collection.create_time, collection.update_time, collection.creator, collection.resource_id)
