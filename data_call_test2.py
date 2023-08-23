import json
import requests
import concurrent.futures
import logging
import uuid
logging.basicConfig(filename='log_file.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = 'http://localhost:8000/transfer/transaction/'


def send_request(url, data):
    response = requests.post(url, json=data)
    return response.json()


data_list = []
for i in range(1000):
    data_list.append(  {
    "source_wallet_id": 15,
    "destination_wallet_id": 17,
    "amount": 1,
    "tracker_id": str(uuid.uuid1()),
    "source_user_id": 10,
    "destination_user_id": 6
  },)

max_threads = 200

# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(send_request, url, data) for data in data_list]

    # Process the results as they become available
    for future, data in zip(concurrent.futures.as_completed(futures), data_list):
        try:
            response = future.result()
            logging.info(f"Response: {response}, Request sent for data: {data}.")
        except Exception as e:
            logging.error(f" Error: {e}, Request failed for data: {data}.")
