import keyboard
import time

def toggle_loop():
    global loop_running
    loop_running = not loop_running

def main_loop():
    loop_count = 0
    text_to_type = "@jaylenwalker., @logan_simmons told me to spam you"  # Replace this with your desired string

    while True:
        if loop_running:
            # Type the specified string
            keyboard.write(text_to_type)
            keyboard.press_and_release("enter")
            
            loop_count += 1
        time.sleep(0.2)  # Adjust the sleep time to achieve the desired loop frequency

# Register the pause button to toggle the loop
keyboard.on_press_key("pause", lambda _: toggle_loop())

# Start the main loop
loop_running = False
main_loop()