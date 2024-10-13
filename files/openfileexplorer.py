from plyer import filechooser

file_paths = filechooser.open_file(multiple=False)
print(file_paths[0])

file_paths = filechooser.open_file(multiple=True, filters=["*.jpeg", "*.jpg"])
print(file_paths)

file_paths = filechooser.open_file(multiple=True)

if file_paths:
    for path in file_paths:
        print("Selected file:", path)
else:
    print("No file selected")


file_path = filechooser.save_file()
print(file_path)
