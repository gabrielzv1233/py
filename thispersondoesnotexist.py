import requests
from plyer import filechooser

url = "https://thispersondoesnotexist.com/"

file_path = filechooser.save_file(title="Save image as", path="person.jpg", filters=[("jpeg image", "*.jpg;*.jpeg")])[0]

if file_path:
    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully saved to {file_path}")
    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
else:
    print("No file path chosen. Exiting...")
