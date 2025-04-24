import base64
import os
import sys

script_location = os.path.dirname(os.path.abspath(sys.argv[0]))

text_file_path = input("Enter the text file path: ")

try:
    with open(text_file_path, "r") as text_file:
        encoded_data = text_file.read()

    file_data = base64.b64decode(encoded_data)

    original_filename = os.path.basename(text_file_path).replace(".txt", "")
    restored_file_path = os.path.join(script_location, original_filename)

    with open(restored_file_path, "wb") as file:
        file.write(file_data)

    print(f"File successfully restored as {restored_file_path}")

except Exception as e:
    print(f"Error: {e}")
