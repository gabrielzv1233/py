import shelve
from flask import Flask, make_response, request 
import uuid
import datetime
app = Flask(__name__)

@app.route("/")
def main():
    db = shelve.open('databases/users/userdata')
    username = request.cookies.get('un')
    login_token = request.cookies.get('LOGIN_TOKEN')
    if not username or not login_token:
        return "not logged in"
    else: 
        if username in db:
            data = db[username]
            if login_token == data[1]:
                db.close()
                return f'logged in as {username}<form method="POST" action="/logout"><input type="submit" value="Logout"></form><br><br><form method="POST" action="/delete_account"><input type="checkbox" required>Check this and click button below to delete account<br><input type="submit" value="Delete account">'
            else:
                db.close()
                return "not logged in"
            
@app.route("/delete_account", methods=["POST"])
def delete_account():
    db = shelve.open('databases/users/userdata')
    username = request.cookies.get('un')
    login_token = request.cookies.get('LOGIN_TOKEN')
    if not username or not login_token:
        return "Unable to delete account: not logged in"
    else:
        if username in db:
            data = db[username]
            if login_token == data[1]:
                del db[username]
                db.close()
                response = make_response("Deleted account")
                response.delete_cookie("LOGIN_TOKEN")
                response.delete_cookie("un")
                response.headers["Location"] = "/"
                return response
            else:
                db.close()
                return "Unable to delete account: not logged in"

@app.route('/logout', methods=["POST"])
def logout():
    response = make_response("Logged out")
    response.delete_cookie("LOGIN_TOKEN")
    response.delete_cookie("un")
    response.headers["Location"] = "/"
    return response, 302

@app.route('/li', methods=['POST'])
def li():
    db = shelve.open('databases/users/userdata')
    username = str(request.form.get('username'))
    password = str(request.form.get('password')) 
    print(username)
    print(password)
    if username in db:
        data = db[username]
        userpass = data[0]
        if password == userpass:
            db.close()
            response = make_response(f"logged in")
            expiration = datetime.datetime.now() + datetime.timedelta(days=365 * 10)
            response.set_cookie('LOGIN_TOKEN', data[1], expires=expiration)
            response.set_cookie('un', username, expires=expiration)
            response.headers["Location"] = "/"
            return response, 302
        else:
            return "login info incorrect"
    else:
        db.close()
        return "login info incorrect"

@app.route('/si', methods=['POST'])
def si():
    db = shelve.open('databases/users/userdata')
    username = str(request.form.get('username'))
    data = [str(request.form.get('password')), str(uuid.uuid4())]
    print(username)
    print(data[0])
    if username in db:
        db.close()
        return "Account already exists"
    else:
        db[username] = data
        response = make_response(f"Created account<br>{username}<br>{str(data)}")
        expiration = datetime.datetime.now() + datetime.timedelta(days=365 * 10)
        response.set_cookie('LOGIN_TOKEN', data[1], expires=expiration)
        response.set_cookie('un', username, expires=expiration)
        response.headers["Location"] = "/"
        db.close()
        return response, 302
       
@app.route("/login")
def login():
    return """<form method="POST" action="/li">
    <input type="text" name="username" required>
    <input type="text" name="password" required>
    <input type="submit" value="login">
</form>"""

@app.route("/signup")
def signup():
    return """<form method="POST" action="/si">
    <input type="text" name="username" required>
    <input type="text" name="password" required>
    <input type="submit" value="signup">
</form>"""


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)