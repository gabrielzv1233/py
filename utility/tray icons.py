from win11toast import toast
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading

def show_notification():
    toast('Notification', 'hu')

def show_left_click_notification(icon, item):
    toast('Left Click', 'Left-clicked the tray icon!')

def create_image():
    # Create an icon image
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill=(0, 0, 0))
    return image

def setup_tray():
    # Create a menu with a default item that will trigger on left-click
    menu = Menu(
        MenuItem('Left-Click Action', action=show_left_click_notification, default=True, visible=False),
        MenuItem('Send Notification', action=show_notification),
        MenuItem('Quit', action=lambda icon, item: icon.stop())
    )
    
    icon = Icon("test_icon", create_image(), "Tray Icon", menu)
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=setup_tray).start()
