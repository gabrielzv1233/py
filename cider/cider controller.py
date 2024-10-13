from flask import Flask, render_template_string, jsonify, request, url_for
import requests

app = Flask(__name__)

icon = "static/favicon.png"

def call_cider(endpoint, request_data):
    response = requests.post(f'http://localhost:10767/api/v1/playback/{endpoint}', json=request_data)
    if response.status_code == 200:
        return response.json()
    return None

def set_vol(request_data):
    response = requests.post(f'http://localhost:10767/api/v1/playback/volume', json=request_data)
    if response.status_code:
        return response.json()

def get_current_volume():
    response = requests.get('http://localhost:10767/api/v1/playback/volume')
    if response.status_code == 200:
        return response.json()
    return {'status': 'error', 'volume': 0}

@app.route('/')
def index():
    volume_data = get_current_volume()
    initial_volume = volume_data.get('volume')
    icon
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
            <link rel="manifest" href="/manifest.json">
            <link rel="icon" href="'''+icon+'''" type="image/png">
            <link rel="apple-touch-icon" href="'''+icon+'''">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="theme-color" content="#212121">
            <title>Cider Control</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                html, body {
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #000;
                    color: #fff;
                }
                .container {
                    display: flex;
                    width: 100%;
                    height: 100%;
                }
                .request-button {
                    flex: 1;
                    font-size: 2em;
                    border: 1px solid #171717;
                    cursor: pointer;
                    background-color: #212121;
                    color: #ececec;
                    user-select: none;
                }
                .request-button:hover, .request-button:active {
                    background-color: #2F2F2F;
                }
                /* iPhone-specific styles */
                .request-button:active {
                    background-color: #3F3F3F;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <button class="request-button" ontouchstart="this.classList.add('hover')" ontouchend="fetch('/action/previous', { method: 'GET' }); this.classList.remove('hover')">Previous</button>
                <button class="request-button" ontouchstart="this.classList.add('hover')" ontouchend="fetch('/action/playpause', { method: 'GET' }); this.classList.remove('hover')">Play/Pause</button>
                <button class="request-button" ontouchstart="this.classList.add('hover')" ontouchend="fetch('/action/next', { method: 'GET' }); this.classList.remove('hover')">Next</button>
            </div>
            <label hidden for="volume-slider">Volume:</label>
            <input hidden type="range" id="volume-slider" step="0.01" min="0" max="1" value="{{ initial_volume }}" onchange="fetch('/set_volume', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ volume: this.value / 100 })
            })" />
        </body>
        </html>
    ''', initial_volume=initial_volume)

@app.route('/action/<endpoint>', methods=['GET', 'POST'])
def action(endpoint):
    data = call_cider(endpoint, {})
    return jsonify(data)

@app.route('/set_volume', methods=['POST'])
def set_volume():
    volume_data = request.get_json()
    volume_value = volume_data['volume']
    data = set_vol({'volume': volume_value})
    return jsonify(data)

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Cider Control",
        "short_name": "Cider Control",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#3f3f3f",
        "theme_color": "#212121",
        "icons": [
            {
                "src": icon,
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10766, debug=True)
