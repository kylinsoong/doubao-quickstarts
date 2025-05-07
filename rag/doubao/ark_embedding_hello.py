import os
import numpy as np
from typing import List
from volcenginesdkarkruntime._exceptions import ArkAPIError
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

resp = client.embeddings.create(
    model=API_EP_ID,
    input=["您好"]
)

print(resp.data)
