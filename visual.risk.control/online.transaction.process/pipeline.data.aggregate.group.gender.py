import json
import os
from pymongo import MongoClient

client = MongoClient()
db = client.risk
collection_name = "simple"
collection = db[collection_name]

pipeline = [
    {
        "$group": {
            "_id": "$vlm.性别",
            "count": {
                "$sum": 1
            }
        }
    }
]

results = collection.aggregate(pipeline)

for result in results:
    print(result)
