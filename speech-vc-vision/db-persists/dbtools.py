import os
import argparse
from urllib.parse import quote_plus
from pymongo import MongoClient

parser = argparse.ArgumentParser(description="MongoDB Document Deletion and Retrieval Script")

parser.add_argument('--delete_all', action='store_true', help="Delete all documents in the collection")
parser.add_argument('--username',  help="The username to be escaped")
parser.add_argument('--password',  help="The password to be escaped")
parser.add_argument('--encode_credentials', action='store_true', help="percent-encode according to RFC 3986")

args = parser.parse_args()

db_url = os.getenv('DB_URL')
db_name = os.getenv('DB_NAME')
db_table = os.getenv('DB_TABLE_NAME')

def get_credentials(username, password):
    # Escape username and password
    escaped_username = quote_plus(username)
    escaped_password = quote_plus(password)

    return escaped_username, escaped_password


try:
    # Connect to MongoDB
    client = MongoClient(db_url)
    database = client[db_name]
    collection = database[db_table]

    if args.encode_credentials:
        escaped_username, escaped_password = get_credentials(args.username, args.password)
        print(escaped_username, escaped_password)
    elif args.delete_all:
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents.")

    else:
        result = collection.find()
        for document in result:
            print(document)

    client.close()

except Exception as e:
    print("An error occurred:", e)
