import pyautogui
import time
import webbrowser
import urllib.parse

def create_bookmarklet(js_code):
    js_code = js_code.replace('\n', '')

    encoded_code = urllib.parse.quote(js_code)

    webbrowser.open("http://www.example.com")
    time.sleep(1)

    pyautogui.hotkey('ctrl', 'e')
    
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite(f"javascript:({encoded_code})()")

    pyautogui.press('enter')

js_code = r'''alert("test")'''

create_bookmarklet(js_code)