from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

def call_cider(request):
    response = requests.get(f'http://localhost:10767/api/v1/playback/{request}')
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <html>
        <head>
            <title>Now Playing</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    display: flex;
                    align-items: center;
                    background-color: white;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: fit-content; /* Set width to fit content */
                    margin: 0 auto; /* Center the container */
                }
                .info {
                    margin-right: 20px;
                }
                .artwork {
                    max-height: 150px; /* Limit image height */
                    border-radius: 10px;
                }
                .explicit {
                    background-color: #212121;
                    color: #ececec;
                    border-radius: 5px;
                    height: 25px; /* Set height */
                    width: 25px; /* Set width to the same as height */
                    display: flex; /* Use flexbox for centering */
                    align-items: center; /* Center vertically */
                    justify-content: center; /* Center horizontally */
                    margin-left: 10px; /* Add more left margin */
                    font-size: 12px; /* Decrease font size */
                    font-weight: bold; /* Make the text bold */
                }
                .song-title-container {
                    display: flex; /* Use flex to align title and explicit tag */
                    align-items: center; /* Center them vertically */
                }
                a.song-title {
                    color: black; /* Black text color */
                    text-decoration: none; /* Remove underline */
                }
                a.song-title:visited {
                    color: black; /* Keep text black when visited */
                }
            </style>
            <script>
                let lastData = null;  // To keep track of the last fetched data

                async function fetchData() {
                    const response = await fetch('/now-playing');
                    const data = await response.json();
                    
                    // Only update if data has changed
                    if (data.error) {
                        document.getElementById('song-info').innerHTML = data.error;
                    } else {
                        // Check if the new data is different from the last
                        if (JSON.stringify(data) !== JSON.stringify(lastData)) {
                            lastData = data; // Update lastData
                            const explicitTag = data.contentRating === "explicit" ? '<span class="explicit">E</span>' : '';
                            document.getElementById('song-info').innerHTML = `
                                <div class="song-title-container">
                                    <a class="song-title" href="https://song.link/i/${data.catalogId}" target="_blank" title="Open with song.link">
                                        <h2 style="margin: 0;">${data.songName}</h2>
                                    </a>
                                    ${explicitTag}
                                </div>
                                <br><strong>Album:</strong> ${data.albumName}<br>
                                <br><strong>Artist:</strong> ${data.artist}
                            `;
                            const img = document.createElement('img');
                            img.src = data.artworkImage;
                            img.alt = 'Album Artwork';
                            img.className = 'artwork';
                            document.getElementById('artwork-container').innerHTML = ''; // Clear previous image
                            document.getElementById('artwork-container').appendChild(img);
                        }
                    }
                }

                // Initial loading message
                document.addEventListener('DOMContentLoaded', () => {
                    document.getElementById('song-info').innerHTML = '<h1>Loading content...</h1>';
                    fetchData(); // Fetch data immediately
                    setInterval(fetchData, 3000);  // Update every 3 seconds
                });
            </script>
        </head>
        <body>
            <div class="container">
                <div class="info" id="song-info"></div>
                <div id="artwork-container"></div>
            </div>
        </body>
    </html>
    ''')

@app.route('/now-playing')
def now_playing():
    data = call_cider("now-playing")
    if data and data.get("status") == "ok":
        info = data.get("info", {})
        
        # Extract artwork URL and replace {w}x{h} with 3000x3000
        artwork_url = info.get("artwork", {}).get("url", "")
        artwork_url = artwork_url.replace("{w}x{h}", "3000x3000")  # Replace dimensions
        
        # Extract catalogId
        catalog_id = info.get("playParams", {}).get("catalogId", "")

        output = {
            "albumName": info.get("albumName"),
            "songName": info.get("name"),
            "contentRating": info.get("contentRating"),
            "artist": info.get("artistName"),
            "artworkImage": artwork_url,
            "catalogId": catalog_id,  # Add catalogId to the output
        }
        return jsonify(output)
    return jsonify({"error": "Failed to retrieve data."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
