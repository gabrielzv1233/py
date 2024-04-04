from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return """<form method="POST" action="/connect">
    <input type="text" name="data" value="post" hidden>
    <input type="submit" value="post">
</form><form method="GET" action="/connect">
    <input type="text" name="data" value="get" hidden>
    <input type="submit" value="get">
</form>"""
    
@app.route("/connect", methods=['GET', 'POST'])
def connect():
    if request.method == 'GET' and not request.is_xhr and not request.is_json:
        return 'Normal connection (not GET or POST).'
    elif request.method == 'GET':
        data = request.args.get('data')
        return data
    elif request.method == 'POST':
        data = request.form["data"]
        return data
    else:
        return "method incorrect"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)