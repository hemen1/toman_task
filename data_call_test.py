import json
import requests
import concurrent.futures
import logging

logging.basicConfig(filename='log_file.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = 'http://localhost:8000/transfer/transaction/'


def send_request(url, data):
    response = requests.post(url, json=data)
    return response.json()


# Open the JSON file for reading
with open('transaction_data.json', 'r') as json_file:
    data_list = json.load(json_file)

max_threads = len(data_list)
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
