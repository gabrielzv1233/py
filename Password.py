import os
import random
import string
import uuid

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special_chars, invalid_chars):
    chars = ''
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_numbers:
        chars += string.digits
    if use_special_chars:
        chars += string.punctuation
    chars = ''.join([c for c in chars if c not in invalid_chars])
    if not chars:
        return "Error: Password must include at least one character set."
    chars = ''.join(random.sample(chars, length))
    return chars

def clear_console():
    if os.name == 'nt':  # for Windows
        os.system("cls")
    else:  # for Linux and macOS
        os.system("clear")
    main()

def main():
    while True:
        length_input = input("Enter password length: ").strip().lower()  # Strip leading/trailing spaces
        if length_input == 'test':
            length, use_uppercase, use_lowercase, use_numbers, use_special_chars, invalid_chars = 10, '?', '?', '?', '?', ''
            password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special_chars, invalid_chars)
            print(password if not password.startswith("Error") else password)
            print()
            continue
        elif length_input == 'clear':
            clear_console()
        elif length_input == 'cls':
            clear_console()
        elif length_input == 'exit':
            exit()
        elif length_input == 'close':
            exit()
        elif length_input == 'stop':
            exit()
        elif length_input == 'ext':
            exit()
        elif length_input == 'uuid':
            try:
                uuid_length = int(input("Enter UUID length (max 36 also includes hyphens): "))
                if uuid_length <= 0:
                    raise ValueError
                uuid_str = str(uuid.uuid4())[:uuid_length]
                print(uuid_str)
                print()
            except ValueError:
                print("Error: Invalid input. Please try again.")
                print()
                continue
        else:
            try:
                length = int(length_input)
                if length <= 0:
                    raise ValueError
                use_uppercase = input("Include uppercase letters? (y/n/?) ").lower()
                if use_uppercase == '?':
                    use_uppercase = random.choice(['y', 'n'])
                if use_uppercase not in ['y', 'n']:
                    raise ValueError
                use_lowercase = input("Include lowercase letters? (y/n/?) ").lower()
                if use_lowercase == '?':
                    use_lowercase = random.choice(['y', 'n'])
                if use_lowercase not in ['y', 'n']:
                    raise ValueError
                use_numbers = input("Include numbers? (y/n/?) ").lower()
                if use_numbers == '?':
                    use_numbers = random.choice(['y', 'n'])
                if use_numbers not in ['y', 'n']:
                    raise ValueError
                use_special_chars = input("Include special characters? (y/n/?) ").lower()
                if use_special_chars == '?':
                    use_special_chars = random.choice(['y', 'n'])
                if use_special_chars not in ['y', 'n']:
                    raise ValueError
                invalid_chars_input = input("Enter invalid characters (separated by spaces): ")
                invalid_chars = ''.join([c.strip() for c in invalid_chars_input.split()])  # Join invalid characters without spaces
                password = generate_password(length, use_uppercase == 'y', use_lowercase == 'y', use_numbers == 'y', use_special_chars == 'y', invalid_chars)
                print(password if not password.startswith("Error") else password)
                print()
            except ValueError:
                print("Error: Invalid input. Please try again.")
                print()
                continue

clear_console()

if __name__ == '__main__':
    main()
