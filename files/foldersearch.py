import os

string = input("search for what: ")  # Case insensitive search

def search_for_string(directory):
    found = 0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if string in line.lower():
                            relative_path = os.path.relpath(file_path, directory)
                            found += 1
                            print(f'Found in {relative_path} on line {i}: {line.strip()}')
            except (UnicodeDecodeError, PermissionError) as e:
                print(f"Could not open {file_path}: {e}")
    print(f"Found {found} instance(s) of {string} in {directory}")

directory_to_search = input("directory: ")
search_for_string(directory_to_search)
