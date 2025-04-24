import base64

file_path = input("Enter the file path: ")

try:
    with open(file_path, "rb") as file:
        file_data = file.read()

    encoded_data = base64.b64encode(file_data).decode()

    output_file = file_path.split("/")[-1] + ".txt"
    with open(output_file, "w") as text_file:
        text_file.write(encoded_data)

    print(f"File successfully converted and saved as {output_file}")

except Exception as e:
    print(f"Error: {e}")
