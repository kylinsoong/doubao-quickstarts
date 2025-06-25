import json
import os
from pymongo import MongoClient

client = MongoClient()
db = client.risk
collection_name = "simple"
collection = db[collection_name]


directory = 'output'

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
            
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)
                
            print(f"Imported {filename} to {collection_name}")
