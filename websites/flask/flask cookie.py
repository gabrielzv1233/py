from flask import Flask, make_response, request
import datetime

app = Flask(__name__)

@app.route('/')
def main():
    response = make_response("Cookie created")
    expiration = datetime.datetime.now() + datetime.timedelta(days=365 * 10)
    response.set_cookie('cookie_name', "cookie_value", expires=expiration)
    return response

@app.route("/read")
def read_cookie():
     return request.cookies.get('cookie_name')

@app.route("/delete")
def delete_cookie():
    response = make_response("Cookie deleted")
    response.delete_cookie("cookie_name")
    return response
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)