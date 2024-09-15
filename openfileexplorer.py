from plyer import filechooser

# Choose 1 file to open
file_paths = filechooser.open_file(multiple=False)
print(file_paths[0])

# Require file to be of select type
file_paths = filechooser.open_file(multiple=True, filters=["*.jpeg", "*.jpg"])
print(file_paths)

# allow opening multiple files
file_paths = filechooser.open_file(multiple=True)

# Print selected file paths
if file_paths:
    for path in file_paths:
        print("Selected file:", path)
        # or handle each file here
else:
    print("No file selected")


# return path for saving a file (works with filter)
file_path = filechooser.save_file()
print(file_path)
