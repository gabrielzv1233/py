import requests

def get_profile(bot_token, user_id):
    url = f"https://discord.com/api/v9/users/{user_id}/profile"
    headers = {
        "accept": "*/*",
        "authorization": bot_token,
        "user-agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), 1
    else:
        return response.status_code, 0
