from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/get', methods=['GET'])
def get():
    data = request.args.get('data')  # Get the value of 'param1'
    # Process the parameters
    return 'Response to the GET request'

@app.route("/")
def main():
    return """<form method="GET" action="/get">
    <input type="text" name="data">
    <input type="submit" value="Submit">
</form>"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)