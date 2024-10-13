import os
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image
import win32com.client

# Define the path to the startup folder
startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')

# Define the path to the script and its name
script_path = sys.argv[0]
shortcut_name = "App.lnk"
shortcut_path = os.path.join(startup_folder, shortcut_name)

# Function to create startup shortcut with --isstartup=True
def create_startup_shortcut():
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = script_path  # Use the correct path to the script/executable
    shortcut.Arguments = '--isstartup=True'  # Pass the --isstartup argument
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.IconLocation = script_path  # Optional: set the icon to your script icon
    shortcut.save()

# Function to enable/disable startup by deleting or creating the shortcut
def toggle_startup(icon, item):
    if os.path.exists(shortcut_path):
        # Disable startup (delete the shortcut)
        os.remove(shortcut_path)
    else:
        # Enable startup (create the shortcut)
        create_startup_shortcut()

    # Update tray icon menu
    icon.update_menu()

# Define the tray icon menu with a toggle
def create_menu():
    return Menu(
        MenuItem(
            'Toggle Startup', toggle_startup, checked=lambda item: os.path.exists(shortcut_path)
        ),
        MenuItem('Exit', lambda icon, item: icon.stop())
    )

# Create the tray icon
def setup_tray_icon():
    icon_image = Image.new('RGB', (64, 64), color=(73, 109, 137))  # Example blank icon
    icon = Icon("MyApp", icon_image, menu=create_menu())
    icon.run()

if __name__ == '__main__':
    # If the script was called with --isstartup=True, you can handle startup-specific logic here
    if '--isstartup=True' in sys.argv:
        print("Started as startup task")
    else:
        # Set up the tray icon with a toggle for startup
        setup_tray_icon()
