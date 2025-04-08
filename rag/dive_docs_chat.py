import json
import requests
import os
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService



collection_name = "investune_docs"
project_name = "project_test_kylin"
query = "中国平安投资价值？"
ak = os.getenv("VE_ACCESS_KEY")
sk = os.getenv("VE_SECRET_KEY")
account_id = os.getenv("VE_ACCOUNT_ID")
g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"

viking_knowledgebase_service = VikingKnowledgeBaseService(host=g_knowledge_base_domain, scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak(ak)
viking_knowledgebase_service.set_sk(sk)

model = "Doubao-pro-32k"
m_messages = [{
    "role": "system",
    "content": """ system pe """
    },
    {
        "role": "user",
        "content": query
    }
]

res = viking_knowledgebase_service.chat_completion(model=model, messages=m_messages, max_tokens=4096, temperature=0.1)


print(res)
