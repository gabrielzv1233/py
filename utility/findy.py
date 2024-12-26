import os
import re
import subprocess
import time

def is_utf8_file(file_path):
    """
    Check if a file is UTF-8 encoded by reading it in small chunks.
    """
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024):  # Read in small chunks
                chunk.decode('utf-8')  # Decode to ensure it's UTF-8
        return True
    except (UnicodeDecodeError, OSError):
        return False

def count_files(folder):
    """
    Count the total number of files in the folder and its subfolders.
    """
    total_files = 0
    for _, _, files in os.walk(folder):
        total_files += len(files)
    return total_files

def search_string_in_files(folder, search_string, skip_count=False):
    """
    Search for a string in UTF-8 files within a folder and its subfolders,
    with optional progress tracking.
    """
    total_files = None
    if not skip_count:
        total_files = count_files(folder)
        print(f"Total files to scan: {total_files}")
    else:
        print("Skipping file count. Scanning directly...")

    scanned_files = 0

    for root, _, files in os.walk(folder):
        for file in files:
            scanned_files += 1
            file_path = os.path.join(root, file)
            found_status = "Not Found"

            if is_utf8_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if re.search(re.escape(search_string), content):
                            found_status = "Found"
                            print(f"Found in: {file_path}")
                            subprocess.run(["explorer", "/select,", os.path.abspath(file_path)])
                except Exception as e:
                    found_status = f"Error ({e})"
            else:
                found_status = "Skipping (Non-UTF-8)"

            # Display progress
            if total_files:
                print(f"Scanning {scanned_files}/{total_files}: {file_path} | {found_status}")
            else:
                print(f"Scanning {scanned_files}: {file_path} | {found_status}")

    print(f"Total files scanned: {scanned_files}")

if __name__ == "__main__":
    folder_to_search = input("Enter the folder to search: ").strip()
    search_term = input("Enter the string to search for: ").strip()
    skip_count_input = input("Skip file count? (yes/no): ").strip().lower()
    skip_count = skip_count_input == "yes"

    if os.path.isdir(folder_to_search):
        search_string_in_files(folder_to_search, search_term, skip_count=skip_count)
    else:
        print("Invalid folder path. Please try again.")
