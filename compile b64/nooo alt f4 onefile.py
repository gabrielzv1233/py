import base64
import io
import pygame
import keyboard
import sys
import os

# Function to load MP3 data from a base64 string
def load_mp3_from_base64(base64_str):
    mp3_data = base64.b64decode(base64_str)
    return io.BytesIO(mp3_data)

mp3_base64 = r"""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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//t4BAAP8AAAaQAAAAgAAA0gAAABAAABpAAAACAAADSAAAAETEFNRQMACQgABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""

# Load MP3 data
mp3_stream = load_mp3_from_base64(mp3_base64)

pygame.mixer.init()
pygame.mixer.music.load(mp3_stream)
keyboard.add_hotkey('Alt+f4', pygame.mixer.music.play)
print("Press Alt+f4 to play the sound, Win+f5 to exit.")
keyboard.wait("win+f5")
