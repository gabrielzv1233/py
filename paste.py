import keyboard
import pyperclip
import time

def override_paste():
    time.sleep(0.1)
    text = pyperclip.paste()[:50]
    keyboard.write(text.strip())

keyboard.add_hotkey('ctrl+v', override_paste, suppress=True)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
