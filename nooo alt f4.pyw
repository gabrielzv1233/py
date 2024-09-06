try:
    import pygame
    import keyboard
    pygame.mixer.init()
    pygame.mixer.music.load(r'AAAAA.mp3')
    keyboard.add_hotkey('Alt+f4', pygame.mixer.music.play)
    print("Press Alt+f4 to play the sound, Win+f5 to exit.")
    keyboard.wait("win+f5")
except KeyboardInterrupt():
    exit(0)