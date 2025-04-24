import base64
import zlib
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
import numpy as np
import pathlib
import subprocess

def compress_and_encode(text):
    compressed_text = text.replace(", ", "").replace("\n", "8")
    compressed_bytes = zlib.compress(compressed_text.encode())
    base64_encoded = base64.urlsafe_b64encode(compressed_bytes).decode()
    return base64_encoded

def parse_text_to_array(text):
    lines = text.strip().split("\n")
    pixel_data = [list(map(int, line.split(", ")[:-1])) for line in lines]
    return np.array(pixel_data, dtype=np.uint8)

def convert_to_image(text):
    color_map = {
        0: (0, 0, 0, 0),
        1: (255, 255, 255),
        2: (255, 0, 0),
        3: (0, 255, 0),
        4: (0, 0, 255),
        5: (0, 255, 255),
        6: (255, 0, 255),
        7: (255, 255, 0),
        8: (0, 0, 0)
    }
    
    pixel_array = parse_text_to_array(text)
    height, width = pixel_array.shape
    image = Image.new("RGBA", (width, height))
    
    for y in range(height):
        for x in range(width):
            image.putpixel((x, y), color_map[pixel_array[y, x]])
    
    return image

def save_image_from_text():
    downloads_path = str(pathlib.Path.home() / "Downloads")
    
    root = tk.Tk()
    root.withdraw()
    
    text_input = tk.simpledialog.askstring("Input", "Paste the text representation of the image:")
    if not text_input:
        print("No input provided.")
        return
    
    compressed_name = compress_and_encode(text_input)[:50]
    output_path = os.path.join(downloads_path, f"{compressed_name}.png")
    
    image = convert_to_image(text_input)
    image.save(output_path)
    subprocess.run(["start", "", output_path], shell=True)
    
if __name__ == "__main__":
    save_image_from_text()
