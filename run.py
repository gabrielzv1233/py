import os
def clear_console():
    if os.name == 'nt':  # for Windows
        os.system("cls")
    else:  # for Linux and macOS
        os.system("clear")
clear_console()
# Dictionary of available apps
apps = {
    1: {
        'label': 'trade.pmc',
        'path': r'"C:\Users\gabri\OneDrive\Documents\trade.pmc"'
    },
    2: {
        'label': 'Blockbench',
        'path': r'C:\Users\gabri\AppData\Local\Programs\Blockbench\Blockbench.exe'
    },
    3: {
        'label': 'MCreator',
        'path': r'C:\Program Files\Pylo\MCreator\mcreator.exe'
    }
}

# Display available apps
print("Available Apps:")
for app_id, app_data in apps.items():
    print(f"{app_id}: {app_data['label']} {app_data['path']}")

# Prompt for app selection
while True:
    selection = input("\nEnter the ID or label (program name) of the app to run: ")
    for app_id, app_data in apps.items():
        if selection.lower() in [str(app_id), app_data['label'].lower()]:
            os.startfile(app_data['path'])
            exit()
    print("Invalid selection. Please try again.")