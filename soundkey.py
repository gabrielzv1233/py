import pygame
import keyboard

# Initialize pygame mixer
pygame.mixer.init()

# Load the sound
sound_file = r'C:\Program Files (x86)\Jingle Palette\Audio_Sample\Import\AAAAA.mp3'
sound = pygame.mixer.Sound(sound_file)

def play_sound():
    sound.play()

# Set up a hotkey to trigger the sound
keyboard.add_hotkey('Home', play_sound)

print("Press Shift+S to play the sound. Press ESC to exit.")
keyboard.wait('esc')  # Wait for the user to press ESC to exit the program
