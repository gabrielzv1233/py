import os
import threading
import pipreqs
from pipreqs import pipreqs
from io import StringIO
import sys

# made this bc i had to reinstall python, entirly made by chatgpt

results = set()
lock = threading.Lock()

def read_requirements(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            with lock:
                results.update(lines)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def analyze_python_dependencies(start_dir):
    temp_stdout = StringIO()
    sys.stdout = temp_stdout

    try:
        pipreqs.get_all_imports(start_dir)
        detected_imports = temp_stdout.getvalue().splitlines()
        with lock:
            results.update(detected_imports)
    except Exception as e:
        print(f"Error analyzing Python files: {e}")
    finally:
        sys.stdout = sys.__stdout__

def find_requirements_and_dependencies(start_dir):
    threads = []

    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.lower() == "all-requirements.txt":
                file_path = os.path.join(root, file)
                thread = threading.Thread(target=read_requirements, args=(file_path,))
                threads.append(thread)
                thread.start()

    py_scan_thread = threading.Thread(target=analyze_python_dependencies, args=(start_dir,))
    threads.append(py_scan_thread)
    py_scan_thread.start()

    for thread in threads:
        thread.join()

    print("\n".join(sorted(results)))

if __name__ == "__main__":
    find_requirements_and_dependencies(r"C:\Users\Gabriel\Documents\vscode")
