import os
import shutil
import time

# Configurations
output_filename = "rules"
output_file_extension = ".sk"
exit_commands = ["exit()", "quit()", "stop()"]
archive_folder = "archive"
styling_prefix = "&c"

# Validate exit commands
if not exit_commands:
    exit("Must have at least one exit command")

# Prepare exit commands
exit_commands = [command.lower() for command in exit_commands]
exit_commands_dir = " or ".join(exit_commands)

# Ask for mode
while True:
    try:
        mode = input("Please choose mode: \"create\", \"continue\"\n>> ").lower()
        if mode == "create" or mode == "continue":
            break
        else:
            print("Error: Invalid mode. Please enter \"create\" or \"continue\".")
    except KeyboardInterrupt:
        confirm_exit = input("\nAre you sure you want to exit? (y/n)\n>> ").lower()
        if confirm_exit == "y":
            exit("Terminated by user")
        elif confirm_exit == "n":
            continue

# Process mode
if mode == "create":
    if os.path.isfile("rules.sk"):
        timestamp = str(int(time.time()))
        new_file_name = output_filename + "_" + timestamp + output_file_extension
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)
        shutil.move(output_filename + output_file_extension, os.path.join(archive_folder, new_file_name))

    index = 1
    print(f"Please enter a rule, and press enter to add another. To finish, type {exit_commands_dir} instead of a rule.\n")
    with open(output_filename + output_file_extension, "w") as f:
        f.write("command /rules:\n    Trigger:")
        while True:
            rule = input("Please enter rule " + str(index) + ": ")
            if rule.lower() in exit_commands:
                print("\nOutputting code in " + output_filename + output_file_extension)
                break
            f.write(f"\n      send \"&lRule {index}:&r {rule}\"")
            index += 1

elif mode == "continue":
    if not os.path.isfile("rules.sk"):
        print(f"Error: {output_filename + output_file_extension} not found. Switching to create mode.")
        with open(output_filename + output_file_extension, "w") as f:
            f.write("command /rules:\n    Trigger:")
        index = 1
    else:
        with open(output_filename + output_file_extension, "a") as f:
            with open(output_filename + output_file_extension, "r") as l:
                index = sum(1 for _ in l) - 1
            index += 1

    print(f"Please enter a rule, and press enter to add another. To finish, type {exit_commands_dir} instead of a rule.\n")
    while True:
        rule = input("Please enter rule " + str(index) + ": ")
        if rule.lower() in exit_commands:
            print("\nOutputting code in " + output_filename + output_file_extension)
            break
        with open(output_filename + output_file_extension, "a") as f:
            f.write(f"\n      send \"&lRule {index}:&r {styling_prefix}{rule}\"")
        index += 1
