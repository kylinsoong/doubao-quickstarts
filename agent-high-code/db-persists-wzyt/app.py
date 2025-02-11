import os
import time
import json
from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db_url = os.getenv('DB_URL')
db_name = os.getenv('DB_NAME')
db_table = os.getenv('DB_TABLE_NAME')

kafka_endpoint = os.getenv('PUB_SUB_EP')
kafka_topic = os.getenv('PUB_SUB_TOPIC_RRSULT')
group_default = 'group-{}'.format(time.time_ns())
reset_default = 'earliest' 
commit_default = 'True'

conf = {
    'bootstrap.servers': kafka_endpoint,  
    'group.id': group_default,
    'auto.offset.reset': reset_default, 
    'enable.auto.commit': commit_default,
    'auto.commit.interval.ms': 1000
}

client = MongoClient(db_url)

def handle_message(msg):
    message = json.loads(msg.value().decode('utf-8'))
    uid = message.get('uid', None)  # Default to None if 'uid' is missing
    url = message.get('url', None) 
    message_type = message.get('type', None)
    video_data = message.get('video', {})

    if not uid or not url or not message_type:
        logging.info("Invalid message: missing uid, url, or type.")
        return

    try: 
        database = client[db_name]
        collection = database[db_table]
   
        existing_document = collection.find_one({'url': url})
        update_data = message

        update_data['type'] = "insert"

        if existing_document:
            update_data['type'] = "upsert"

        update_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))

        if isinstance(video_data, str):
            try:
                video_data = json.loads(video_data)  # Convert string to object if it's valid JSON
            except json.JSONDecodeError:
                logging.warning(f"Invalid JSON format for video data: {video_data}")
                video_data = {"raw_data": video_data} 
        update_data['video'] = video_data

        result = collection.update_one(
            {'url': message['url']},  
            {'$set': update_data},  
            upsert=True  
        )

        if result.upserted_id:
            logging.info(f"Added {message_type} results with UID {uid} and URL {url} to the database.")
        else:
            logging.info(f"Updated existing results with UID {uid} and URL {url} in the database, append {message_type} results")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        client.close()


consumer = Consumer(conf)
consumer.subscribe([kafka_topic])
logging.info(f"Create consumer: {consumer} subscribe to {kafka_topic}")


while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    elif not msg.error():
        handle_message(msg)
    elif msg.error().code() == KafkaError._PARTITION_EOF:
        logging.info('已经到达分区末尾')
    else:
        logging.info('消费消息时出错: %s' % msg.error())
