import time
import itertools
import keyboard
def brute_force_dial_lock():
    digits = int(input("Enter the number of digits in the PIN: "))
    delay = float(input("Enter delay between key presses (in seconds): "))
    stop_key = input("Enter the stop key(s) (e.g., 'ctrl c' for Ctrl+C): ").strip().split()

    print(f"Starting in 3 seconds... Please tab into the target window.")
    time.sleep(3)  
    pin_combinations = itertools.product(range(10), repeat=digits)
    current_state = [0] * digits

    print("Starting brute force...")
    for pin_tuple in pin_combinations:
        pin = list(map(int, pin_tuple))
        print(f"Trying PIN: {''.join(map(str, pin))}")  
        for i, target_digit in enumerate(pin):
            current_digit = current_state[i]
            diff = (target_digit - current_digit) % 10  
            for _ in range(diff):  
                keyboard.press_and_release('up')
                time.sleep(delay)  

            current_state[i] = target_digit  
            if i < digits - 1:
                keyboard.press_and_release('right')
                time.sleep(delay)
        keyboard.press_and_release('enter')
        time.sleep(delay)  
        keyboard.press_and_release('enter')  
        time.sleep(delay)  
        if all(keyboard.is_pressed(k) for k in stop_key):
            print("Stop key detected. Exiting brute force...")
            break
        for _ in range(digits - 1):  
            keyboard.press_and_release('left')
            time.sleep(delay)

    print("Brute force completed.")
if __name__ == "__main__":
    brute_force_dial_lock()
