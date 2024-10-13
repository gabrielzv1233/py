import requests

def call_cider(endpoint, request_data):
    response = requests.post(f'http://localhost:10767/api/v1/playback/{endpoint}', json=request_data)
    if response.status_code:
        return response.json()

request_data = {"volume": 0.2}

endpoint = "volume"

data = call_cider(endpoint, request_data)
print(data)