import shelve
from flask import Flask, make_response, request, session, redirect, url_for
from markupsafe import escape
import uuid
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def main():
    if 'username' not in session or 'login_token' not in session:
        return "Not logged in"
    else:
        username = session['username']
        login_token = session['login_token']
        db = shelve.open('databases/users/userdata')
        if username in db:
            data = db[username]
            if login_token == data[1]:
                db.close()
                return f'Logged in as {escape(username)}<form method="POST" action="/logout"><input type="submit" value="Logout"></form><br><br><form method="POST" action="/delete_account"><input type="checkbox" required>Check this and click button below to delete account<br><input type="submit" value="Delete account">'
            else:
                db.close()
                return "Not logged in"

@app.route("/delete_account", methods=["POST"])
def delete_account():
    if 'username' not in session or 'login_token' not in session:
        return "Unable to delete account: not logged in"
    else:
        username = session['username']
        login_token = session['login_token']
        db = shelve.open('databases/users/userdata')
        if username in db:
            data = db[username]
            if login_token == data[1]:
                del db[username]
                db.close()
                session.pop('username', None)
                session.pop('login_token', None)
                return redirect("/")
            else:
                db.close()
                return "Unable to delete account: not logged in"

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('username', None)
    session.pop('login_token', None)
    return redirect("/")

@app.route('/li', methods=['POST'])
def li():
    db = shelve.open('databases/users/userdata')
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    if username in db:
        data = db[username]
        userpass = data[0]
        if password == userpass:
            db.close()
            session['username'] = username
            session['login_token'] = data[1]
            return redirect("/")
        else:
            return "Login info incorrect"
    else:
        db.close()
        return "Login info incorrect"

@app.route('/si', methods=['POST'])
def si():
    db = shelve.open('databases/users/userdata')
    username = str(request.form.get('username'))
    data = [str(request.form.get('password')), str(uuid.uuid4())]
    if username in db:
        db.close()
        return "Account already exists"
    else:
        db[username] = data
        db.close()
        session['username'] = username
        session['login_token'] = data[1]
        return redirect("/")

@app.route("/login")
def login():
    if 'username' in session and 'login_token' in session:
        return redirect("/")
    return """<form method="POST" action="/li">
    <input type="text" name="username" required>
    <input type="text" name="password" required>
    <input type="submit" value="Login">
</form>"""

@app.route("/signup")
def signup():
    if 'username' in session and 'login_token' in session:
        return redirect("/")
    return """<form method="POST" action="/si">
    <input type="text" name="username" required>
    <input type="text" name="password" required>
    <input type="submit" value="Signup">
</form>"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)