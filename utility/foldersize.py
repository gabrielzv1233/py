import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size / (1024 ** 3)

folder_path = input("Enter the folder location: ")
size_in_gb = get_folder_size(folder_path)
print(f"Total size of '{folder_path}' is {size_in_gb:.2f} GB")
