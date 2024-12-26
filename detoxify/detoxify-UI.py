from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
from detoxify import Detoxify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ermwhatthesigma'
socketio = SocketIO(app)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Analyzer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; background-color: #202123; color: #D1D5DB; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; padding: 0; text-align: center; }
        #app { background-color: #292b2f; padding: 20px; border-radius: 8px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2); display: flex; flex-direction: column; align-items: center; min-width: 40vw; max-width: 95vw; max-height: 95vh; overflow-y: auto; }
        textarea { padding: 10px; border: none; border-radius: 5px; font-size: 1rem; outline: none; resize: none; overflow-y: auto; line-height: 1.5em; width: 100%; max-width: 100%; margin-bottom: 5px; min-height: 1.5em; }
        button { width: 25%; background-color: #2D8CFF; color: white; border: none; padding: 10px 15px; font-size: 1rem; border-radius: 5px; cursor: pointer; transition: background-color 0.3s; margin-top: 10px; }
        button:disabled { background-color: #525357; cursor: not-allowed; }
        #response { margin-top: 15px; color: #E5E7EB; width: 100%; max-width: 95%; text-align: center; white-space: pre-wrap; word-wrap: break-word; }
        h2 { margin-bottom: 5px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.min.js"></script>
</head>
<body>
    <div id="app">
        <h2>Text Analyzer</h2>
        <textarea id="inputText" placeholder="Enter text to analyze"></textarea>
        <button id="sendButton" onclick="doAnalysis()">Analyze</button>
        <div id="response"></div>
    </div>
    <script>
        const socket = io();
        const sendButton = document.getElementById('sendButton');
        const inputText = document.getElementById('inputText');
        const responseDiv = document.getElementById('response');
        const appDiv = document.getElementById('app');
        function resizeApp() {
            const maxAvailableHeight = window.innerHeight * 0.95;
            appDiv.style.maxHeight = `${maxAvailableHeight}px`;
            const maxTextareaHeight = maxAvailableHeight - (appDiv.offsetHeight - inputText.offsetHeight);
            inputText.style.maxHeight = `${maxTextareaHeight}px`;
        }
        function heighthing() { resizeApp(); requestAnimationFrame(heighthing); }
        heighthing();
        function resizeText() { inputText.style.height = 'auto'; inputText.style.height = `${inputText.scrollHeight}px`; }
        resizeText();
        inputText.addEventListener('input', resizeText);
        function doAnalysis() {
            const text = inputText.value;
            if (!text) { responseDiv.textContent = "Please enter some text."; return; }
            sendButton.disabled = true;
            responseDiv.textContent = "Analyzing...";
            const timeout = setTimeout(() => {
                sendButton.disabled = false;
                responseDiv.textContent = "Error: Request timed out.";
            }, 15000);
            socket.emit('analyze_text', { text });
            socket.on('response', (data) => {
                clearTimeout(timeout);
                sendButton.disabled = false;
                if (data.success) {
                    responseDiv.innerHTML = `<pre>${data.message}</pre>`;
                } else {
                    responseDiv.textContent = data.message;
                }
            });
        }
        inputText.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey && !sendButton.disabled) {
                event.preventDefault();
                doAnalysis();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html)

@socketio.on('analyze_text')
def text_analysis(data):
    text = data.get('text', '')
    try:
        results = Detoxify('original').predict(text)
        response_text = "\n".join(f"{category.capitalize()}: {score:.2f}" for category, score in results.items())
        emit('response', {'success': True, 'message': response_text})
    except Exception as e:
        emit('response', {'success': False, 'message': f"Error: {str(e)}"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
