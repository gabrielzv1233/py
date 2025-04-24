import tkinter as tk
from tkinter import filedialog
import subprocess
import os
from PIL import Image
import time
import uuid

import base64
import zlib

def compress_and_encode(text):
    compressed_text = text.replace(", ", "").replace("\n", "8")
    compressed_bytes = zlib.compress(compressed_text.encode())
    base64_encoded = base64.urlsafe_b64encode(compressed_bytes).decode()
    return base64_encoded


output_file = str

colors = {
        (255, 255, 255): 0,  # White
        (255, 0, 0): 1,       # Red
        (0, 255, 0): 2,       # Green
        (0, 0, 255): 3,       # Blue
        (0, 255, 255): 4,     # Cyan
        (255, 0, 255): 5,     # Magenta
        (255, 255, 0): 6,     # Yellow
        (0, 0, 0): 7          # Black
    }

def closest_color(rgb):
    global colors
    return min(colors, key=lambda c: sum((c[i] - rgb[i]) ** 2 for i in range(3)))

def process_image(image_path, output_file):
    global colors
    
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    
    with open(output_file, 'w') as f:
        for y in range(height):
            row_values = ["0"]  # Start with a leading shift
            for x in range(width):
                r, g, b, a = img.getpixel((x, y))
                if a == 0:  # Fully transparent pixel
                    row_values.append("0")
                else:
                    color = closest_color((r, g, b))
                    row_values.append(str(colors[color]))
            f.write(", ".join(row_values) + "\n")  # Add newline after each row

def main():
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    
    if not image_path:
        print("No file selected.")
        return
    
    process_image(image_path, output_file)
    
    subprocess.run(["start", "", "code", output_file], shell=True)
    time.sleep(1)
    os.remove(output_file)
    print("Output file deleted.")

if __name__ == "__main__":
    main()