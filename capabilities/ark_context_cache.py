import os
import datetime
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
model = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

if __name__ == "__main__":
    print("----- create context -----")
    
    response = client.context.create(
        model=model,
        mode="session",
        messages=[
            {"role": "system", "content": "你是李雷"},
        ],
        ttl=datetime.timedelta(minutes=60),
    )

    print(response)
