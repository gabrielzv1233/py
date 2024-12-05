import requests

def call_cider(request):
    response = requests.get(f'http://localhost:10767/api/v1/playback/{request}')
    if response.status_code == 200:
        return response.json()
    return None

def print_values(data):
    def recursive_print(data, prefix=""):
        if isinstance(data, dict):
            for key, value in data.items():
                recursive_print(value, f"{prefix}{key}.")
        elif isinstance(data, list):
            for index, item in enumerate(data):
                recursive_print(item, f"{prefix}{index}.")
        else:
            print(f"{prefix[:-1]}: {data}")

    if isinstance(data, dict):
        status = data.get("status")
        if status == "ok":
            info = data.get("info", {})
            recursive_print(info)

data = call_cider("now-playing")
print("Raw JSON:\n"+ str(data)+"\n\nFormatted JSON:")
print_values(data)