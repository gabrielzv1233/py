from plyer import filechooser
from PIL import Image
import os

# Open file explorer to choose the source image
source_path = filechooser.open_file(title="Select an Image", filters=[("Image files", '*.jpeg;*.jpg;*.bmp;*.gif;*.tiff')])

if source_path:
    source_path = source_path[0]  # filechooser returns a list, we need the first element
    img = Image.open(source_path)

    # Open file explorer to choose the destination directory
    dest_dir = filechooser.save_file()

    if dest_dir:
        dest_dir = dest_dir[0]
        filename = os.path.basename(source_path).split('.')[0] + '.png'  # Keep the same name but change the extension
        dest_path = os.path.join(dest_dir, filename)

        # Save the image as PNG
        img.save(dest_path, "PNG")
        print(f"Image saved as PNG at: {dest_path}")
    else:
        print("No destination folder selected.")
else:
    print("No source file selected.")
