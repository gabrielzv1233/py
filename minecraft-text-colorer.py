import pyperclip
import os
import sys
import random
def clear_console():
    if os.name == 'nt':  # for Windows
        os.system("cls")
    else:  # for Linux and macOS
        os.system("clear")

clear_console()

def color_text(text):
    color_codes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    result = ""
    for char in text:
        color_code = "&" + random.choice(color_codes)
        result += color_code + char
    return result
loop = True
while loop == True:
    input_text = input("Please input some text to be colored: ")
    if input_text == "clear":
        clear_console()
        sys.stdout.write("Please input some text to be colored: ")
        print(input_text)
    colored_text = color_text(input_text)
    print(colored_text)
    pyperclip.copy(colored_text)