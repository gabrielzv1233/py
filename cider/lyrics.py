import requests
import time

BASE_URL = "http://localhost:10767/api/v1"
LYRIC_DELAY_OFFSET = -0.7
LOOP_DELAY = 0.1

PRINT_START_TIME = True
PRINT_END_TIME = False  # Disabled by default

def get_song_info():
    response = requests.get(f"{BASE_URL}/playback/now-playing")
    song_info = response.json()
    
    if song_info.get("status") != "ok":
        raise ValueError("API returned an error status.")
    
    info = song_info["info"]
    current_time = info.get("currentPlaybackTime", 0)
    
    try:
        song_id = info["playParams"]["id"]
    except KeyError:
        raise KeyError("'playParams' key not found in song info.")
    
    return current_time, song_id

def get_lyrics(song_id):
    lyrics_url = f"{BASE_URL}/lyrics/{song_id}"
    lyrics_response = requests.get(lyrics_url)
    lyrics = lyrics_response.json()

    return lyrics

def find_current_lyric(playback_time, lyrics):
    for line in lyrics:
        if line['start'] <= playback_time <= line['end']:
            return line
    return None

try:
    lyrics = None
    current_song_id = None
    last_displayed_lyric = None
    no_lyric_displayed = False
    
    while True:
        try:
            current_time, song_id = get_song_info()
            adjusted_time = current_time - LYRIC_DELAY_OFFSET
            
            if song_id != current_song_id:
                lyrics = get_lyrics(song_id)
                current_song_id = song_id
            
            current_lyric = find_current_lyric(adjusted_time, lyrics)
            
            if current_lyric and current_lyric != last_displayed_lyric:
                if PRINT_START_TIME:
                    print(f"[{current_lyric['start']:.2f}] ", end="")
                print(current_lyric['text'], end="")
                if PRINT_END_TIME:
                    print(f" [{current_lyric['end']:.2f}]")
                else:
                    print()
                last_displayed_lyric = current_lyric
                no_lyric_displayed = False
            elif not current_lyric and not no_lyric_displayed:
                print()
                no_lyric_displayed = True
            
            time.sleep(LOOP_DELAY)

        except KeyError as e:
            print(f"Key error occurred: {e}")
            break

except KeyboardInterrupt:
    exit(0)
