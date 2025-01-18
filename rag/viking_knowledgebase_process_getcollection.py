import os
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService, Collection, Doc, Point
from volcengine.viking_knowledgebase.common import Field, FieldType, IndexType, EmbddingModelType

access_key     = os.environ.get("IAM_AK")
secret_key     = os.environ.get("IAM_SK")
vkb_host       = os.environ.get("VKB_HOST")
vkb_collection = os.environ.get("VKB_COLLECTION")
vkb_project    = os.environ.get("VKB_PROJECT")

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
