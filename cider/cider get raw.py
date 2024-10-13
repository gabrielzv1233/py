import requests

def call_cider(request):
    response = requests.get(f'http://localhost:10767/api/v1/playback/{request}')
    if response.status_code == 200:
        return response.json()
    return None

data = call_cider("volume")
print(data)
