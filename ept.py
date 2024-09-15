import os
import sys
import time
def check_executable_info():
    # sys.executable: Points to the Python interpreter or the compiled executable
    print(f"sys.executable: {sys.executable}")
    
    # sys.argv[0]: The path to the script or executable being run
    print(f"sys.argv[0]: {sys.argv[0]}")
    
    # os.path.realpath(__file__): Absolute path to the current script or executable
    print(f"os.path.realpath(__file__): {os.path.realpath(__file__)}")
    
    # sys._MEIPASS: Temporary directory PyInstaller uses for the bundled files
    if getattr(sys, 'frozen', False):
        print(f"sys._MEIPASS (PyInstaller temp dir): {sys._MEIPASS}")
    else:
        print("sys._MEIPASS is not available (not a PyInstaller executable)")
    
    # Detect if running as a compiled executable
    if getattr(sys, 'frozen', False):
        print("Running as a compiled executable (PyInstaller).")
    else:
        print("Running as a Python script.")

if __name__ == '__main__':
    check_executable_info()
    time.sleep(100)
