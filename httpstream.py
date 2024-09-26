from flask import Flask, Response, send_from_directory
import mss
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

# Directory to serve static files (for the HTML page)
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')

def generate_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Capture the first monitor
        while True:
            # Capture the screen
            img = sct.grab(monitor)
            # Convert to PIL Image
            pil_image = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
            # Convert PIL Image to bytes
            buffer = io.BytesIO()
            pil_image.save(buffer, format="JPEG")
            frame = buffer.getvalue()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Ensure the static directory exists
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    # Create a simple HTML file for the video feed
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Screen Stream</title>
        <style>
            body {
                margin: 0;
            }
        </style>
    </head>
    <body>
        <img src="/video_feed" width="100%" height="auto">
    </body>
    </html>
    """
    
    with open(os.path.join(STATIC_DIR, 'index.html'), 'w') as f:
        f.write(html_content)
    
    app.run(host='0.0.0.0', port=5000)
