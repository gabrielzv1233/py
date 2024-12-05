import time
import os
import json

json_string = input("Paste JSON here (Should be formatted in one line):\n>> ")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(0.1)

def display_keys(data, current_path="/"):
    clear_console()
    print("Available keys at this level:")
    for key, value in data.items():
        value_type = type(value).__name__
        print(f"{key}: {value_type}")
    print("\nCurrent path:", current_path)

def navigate_data(data, current_path="/"):
    while True:
        display_keys(data, current_path)
        try:
            if current_path == "/":
                key = input("\nEnter a key to navigate or 'exit' to quit: ")
            else:
                key = input("\nEnter a key to navigate or 'back' to go up a level: ")

            if current_path == "/" and key.lower() == 'exit':
                print("Exiting the program...")
                return None

            if key == 'back' and current_path != "/":
                return None

            if key not in data:
                clear_console()
                print(f"Invalid key: {key}. Please try again.\n")
                continue

            value = data[key]
            value_type = type(value).__name__
            new_path = f"{current_path}/{key}".replace("//", "/")

            if isinstance(value, dict):
                result = navigate_data(value, new_path)
                if result is None:
                    continue
                else:
                    return result
            elif isinstance(value, list):
                clear_console()
                print(f"{new_path} is a list with {len(value)} elements.\n{value}")
                input("\nPress Enter to continue...")
            else:
                clear_console()
                print(f"{new_path}: {value_type} = {value}")
                input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            if current_path == "/":
                return None
            else:
                return None

try:
    data = json.loads(json_string)
    navigate_data(data)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")