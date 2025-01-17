import os
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService, Collection, Doc, Point
from volcengine.viking_knowledgebase.common import Field, FieldType, IndexType, EmbddingModelType

access_key = os.environ.get("IAM_AK")
secret_key = os.environ.get("IAM_SK")
vkb_host = os.environ.get("VKB_HOST")
vkb_collection = os.environ.get("VKB_COLLECTION")

viking_knowledgebase_service = VikingKnowledgeBaseService(host=vkb_host, scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak(access_key)
viking_knowledgebase_service.set_sk(secret_key)

my_collection = viking_knowledgebase_service.get_collection(collection_name=vkb_collection)

print(my_collection)
