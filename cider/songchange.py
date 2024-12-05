import requests
import time
import os
import sys
from win11toast import notify

BASE_URL = "http://localhost:10767/api/v1"
LOOP_DELAY = 1

def get_song_info():
    response = requests.get(f"{BASE_URL}/playback/now-playing")
    song_info = response.json()
    
    if song_info.get("status") != "ok":
        raise ValueError("API returned an error status.")
    
    info = song_info["info"]
    
    try:
        song_id = info["playParams"]["id"]
        catalog_id = info["playParams"].get("catalogId", None)
        song_name = info["name"]
        artist_name = info["artistName"]
        album_name = info["albumName"]
        album_icon_url = info["artwork"]["url"].replace("{w}x{h}", f"{info['artwork']['width']}x{info['artwork']['height']}")
        
    except KeyError as e:
        raise KeyError(f"Missing key in song info: {e}")
    
    return song_id, catalog_id, song_name, artist_name, album_name, album_icon_url

def download_image(image_url, filename):
    if os.path.exists(filename):
        os.remove(filename)
    
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

def placeholder_function(song_name, artist_name, album_name, album_icon_url, catalog_id):
    download_image(album_icon_url, os.path.join(os.path.dirname(sys.argv[0]), "CurrentSongIcon.png"))
    notify(f"{song_name} by {artist_name}", album_name, on_click=f'https://song.link/i/{catalog_id}', image=os.path.join(os.path.dirname(sys.argv[0]), "CurrentSongIcon.png"), audio={'silent': 'true'})
    time.sleep(0.1)
    os.remove(os.path.join(os.path.dirname(sys.argv[0]), "CurrentSongIcon.png"))

try:
    last_song_id = None
    
    while True:
        try:
            song_id, catalog_id, song_name, artist_name, album_name, album_icon_url = get_song_info()
            
            if song_id != last_song_id:
                placeholder_function(song_name, artist_name, album_name, album_icon_url, catalog_id)
                last_song_id = song_id
            
            time.sleep(LOOP_DELAY)

        except KeyError as e:
            print(f"Key error occurred: {e}")
            break
except KeyboardInterrupt:
    exit(0)
