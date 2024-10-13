from flask import Flask, request

app = Flask(__name__)

@app.route("/post", methods=["POST"])
def post():
    data = request.form["data"]
    return data
    
@app.route("/")
def main():
    return """<form method="POST" action="/post">
    <input type="text" name="data">
    <input type="submit" value="Submit">
</form>"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)