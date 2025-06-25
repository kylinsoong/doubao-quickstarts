import json
import os
from pymongo import MongoClient

client = MongoClient()
db = client.risk
collection_name = "simple"
collection = db[collection_name]

pipeline = [
    {
        '$match': {
            'vlm.异常': {
                '$ne': '无'
            }
        }
    }, {
        '$count': 'totoal'
    }
] 


results = collection.aggregate(pipeline)

for result in results:
    print(result)
