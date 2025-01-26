import os
import requests
import time
import json

# API Endpoints
SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

# Read API keys from system environment variables
API_APP_KEY = os.getenv("ASR_API_APP_KEY")
API_ACCESS_KEY = os.getenv("ASR_API_ACCESS_KEY")
API_REQUEST_ID = os.getenv("ASR_API_REQUEST_ID")
API_RESOURCE_ID = os.getenv("ASR_API_RESOURCE_ID")
API_SEQUENCE = os.getenv("ASR_API_SEQUENCE", "-1")  # Default to "-1"

# Validate environment variables
if not all([API_APP_KEY, API_ACCESS_KEY, API_RESOURCE_ID]):
    raise EnvironmentError("Environment variables DOUBAO_API_APP_KEY, DOUBAO_API_ACCESS_KEY, and DOUBAO_API_RESOURCE_ID must be set.")

# Submit API function
def submit_task(payload_file):

    print("submit task...")

    # Load payload from file
    with open(payload_file, 'r') as file:
        payload = json.load(file)

    # Headers for the Submit API
    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": API_APP_KEY,
        "X-Api-Access-Key": API_ACCESS_KEY,
        "X-Api-Resource-Id": API_RESOURCE_ID,
        "X-Api-Request-Id": API_REQUEST_ID,
        "X-Api-Sequence": API_SEQUENCE,
    }

    # Send POST request to the Submit API
    response = requests.post(SUBMIT_URL, headers=headers, json=payload)

    print("response status_code", response.status_code)

    if response.status_code == 200:
        time.sleep(3)
        return API_REQUEST_ID
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return None

def query_task(request_id):

    print("query task...")

    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": API_APP_KEY,
        "X-Api-Access-Key": API_ACCESS_KEY,
        "X-Api-Resource-Id": API_RESOURCE_ID,
        "X-Api-Request-Id": API_REQUEST_ID,
    }

    while True:
        response = requests.post(QUERY_URL, headers=headers, json={})
        if response.status_code == 200:
            data = response.json()
            text = data['result']['text']
            print(text)
            break
        else:
            print(f"HTTP Error: {response.status_code}")
            print(response.text)


if __name__ == "__main__":
    payload_file = "payload.json"  # Replace with your actual payload file path

    request_id = submit_task(payload_file)
    if request_id:
        query_task(request_id)

