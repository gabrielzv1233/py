import pyautogui
import time
import webbrowser
import urllib.parse

def create_bookmarklet(js_code):
    # Remove newline characters from the JavaScript code
    js_code = js_code.replace('\n', '')

    # Encode the JavaScript code as a bookmarklet
    encoded_code = urllib.parse.quote(js_code)

    # Open a new browser tab with google.com
    webbrowser.open("http://www.example.com")
    time.sleep(1)  # Wait for the new tab to open

    # Simulate the keyboard shortcut to enter the URL bar using Ctrl+E
    pyautogui.hotkey('ctrl', 'e')
    
    time.sleep(1)  # Wait for the URL bar to become active
    pyautogui.hotkey('ctrl', 'a')
    # Type the JavaScript code as a bookmarklet
    pyautogui.typewrite(f"javascript:({encoded_code})()")

    # Press Enter to execute the JavaScript code
    pyautogui.press('enter')

# JavaScript code to execute as a bookmarklet
js_code = r'''alert("test")'''

# Execute the JavaScript code as a bookmarklet in the browser
create_bookmarklet(js_code)