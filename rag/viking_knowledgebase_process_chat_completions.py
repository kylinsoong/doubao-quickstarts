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

query = "2024前三季新华保险银保新单期限结构趋势"

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
