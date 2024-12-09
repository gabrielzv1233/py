import os
import msvcrt
import random
import time


password = ''.join(str(random.randint(0, 9)) for _ in range(4))
password = "0014"

cursor_position = 0
running = True
user_attempt = ['0'] * len(password)
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def display_lock():
    clear_console()
    print(" ".join("^" if i == cursor_position else " " for i in range(len(user_attempt))))
    print(" ".join(user_attempt))
    print(" ".join("v" if i == cursor_position else " " for i in range(len(user_attempt))))
    print()
    print("Password is: " + password)

def get_key():
    key = msvcrt.getch()
    if key == b'\xe0':
        key = msvcrt.getch()
        return key
    return key

def show_message_and_wait(message, timeout=5):
    clear_console()
    print(message)
    start_time = time.time()
    while time.time() - start_time < timeout:
        if msvcrt.kbhit() and msvcrt.getch() == b'\r':
            break

display_lock()
while running:
    key = get_key()

    if key == b'H':
        user_attempt[cursor_position] = str((int(user_attempt[cursor_position]) + 1) % 10)
        display_lock()
    elif key == b'P':
        user_attempt[cursor_position] = str((int(user_attempt[cursor_position]) - 1) % 10)
        display_lock()
    elif key == b'K':
        cursor_position = (cursor_position - 1) % len(user_attempt)
        display_lock()
    elif key == b'M':
        cursor_position = (cursor_position + 1) % len(user_attempt)
        display_lock()
    elif key == b'\r':
        entered_pin = ''.join(user_attempt)
        if entered_pin == password:
            print("Access Granted!")
            running = False
        else:
            show_message_and_wait("Password Incorrect. Try Again.", timeout=5)
            display_lock()
    elif key == b'\x1b':
        running = False
        print("Exiting...")
        break