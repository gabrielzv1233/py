
from pypresence import Presence
from flask import Flask, make_response, request
from datetime import datetime, timezone, timedelta
from win11toast import notify

YourUsername = "Gabrielzv1233"
EnableRatelimit = True #limits to 1x per minute
client_id = 'bot client id'

app = Flask(__name__)


RPC = Presence(client_id) 
RPC.connect()

RPC.update(
    large_image="wave", # Must upload image to bot's Rich Presence Assets, put name of asset here (i uploaded wave.png so i set it to wave)
    large_text="Hello",
    details="Click the button and I'll get a notification",
    state=None,
    buttons=[{"label":"Say hi","url":r"http://discordstatus.gabrielzv1233.net"}]
)

@app.route('/')
def main():
    if not EnableRatelimit or 'Sent' not in request.cookies:
        notify('Someone says hello!', duration='short')
        response = make_response(f"Sent a notification to {YourUsername}'s device, you can do this again in 1 minute")
        if EnableRatelimit:
            expiration = datetime.now(timezone.utc) + timedelta(minutes=1)
            response.set_cookie('Sent', expiration.strftime('%Y-%m-%d %H:%M:%S.%f%z'), expires=expiration)
        return response
    else:
        expires = datetime.strptime(request.cookies.get('Sent'), '%Y-%m-%d %H:%M:%S.%f%z')
        remaining_time = expires - datetime.now(timezone.utc)
        
        remaining_minutes = int((remaining_time.total_seconds() % 3600) // 60)
        remaining_seconds = int(remaining_time.total_seconds() % 60)
        
        time_parts = []
        if remaining_minutes > 0:
            time_parts.append(f"{remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}")
        if remaining_seconds > 0:
            time_parts.append(f"{remaining_seconds} second{'s' if remaining_seconds != 1 else ''}")
        
        if not time_parts:
            return "An error has occurred"
        
        time_str = " and ".join(time_parts)
        
        return f"You cannot do this yet :( check back in {time_str}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4919)
