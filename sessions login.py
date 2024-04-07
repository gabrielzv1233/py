import shelve
from flask import Flask, request, session, redirect, url_for
import uuid
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()
print(app.secret_key)

@app.route("/")
def main():
    if 'username' not in session or 'login_token' not in session:
        return "not logged in"

    username = session['username']
    login_token = session['login_token']
    db = shelve.open('databases/users/userdata')
    if username in db:
        data = db[username]
        if login_token == data[1]:
            db.close()
            return f'logged in as {username}<form method="POST" action="/logout"><input type="submit" value="Logout"></form><br><br><form method="POST" action="/delete_account"><input type="checkbox" required>Check this and click button below to delete account<br><input type="submit" value="Delete account">'
    
    db.close()
    return "not logged in"

@app.route("/delete_account", methods=["POST"])
def delete_account():
    if 'username' not in session or 'login_token' not in session:
        return "Unable to delete account: not logged in"

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
            return redirect(url_for('main'))

    db.close()
    return "Unable to delete account: not logged in"

@app.route("/signup")
def signup():
    return """<form method="POST" action="/si">
    username: <input type="text" name="username" required><br>
    password: <input type="text" name="password" required><br>
    <input type="submit" value="signup">
</form>"""

@app.route("/login")
def login():
    return """<form method="POST" action="/li">
    username: <input type="text" name="username" required><br>
    password: <input type="text" name="password" required><br
    <input type="submit" value="login">
</form>"""

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('username', None)
    session.pop('login_token', None)
    return redirect(url_for('main'))

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
            return redirect(url_for('main'))
    
    db.close()
    return "login info incorrect"

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
        return redirect(url_for('main'))

@app.route("/admin/signup")
def admin_signup():
    return """<form method="POST" action="/admin/_signup">
    admin key: <input type="text" name="admin_key" required><br>
    username: <input type="text" name="username" required><br>
    password: <input type="text" name="password" required><br>
    <input type="submit" value="signup">
</form>"""

@app.route('/admin/_signup', methods=['POST'])
def api_admin_signup():
    db = shelve.open('databases/users/admindata')
    admin_login_key = str(request.form.get('admin_key'))
    username = str(request.form.get('username'))
    data = [str(request.form.get('password')), str(uuid.uuid4())]
    if not admin_login_key == "3gr978":
        return "Admin key incorrect"
    if username in db:
        db.close()
        return "Account already exists"
    else:
        db[username] = data
        db.close()
        session['admin_username'] = username
        session['admin_login_token'] = data[1]
        return redirect(url_for('admin'))

@app.route("/admin/login")
def admin_login():
    return """<form method="POST" action="/admin/login">
    username: <input type="text" name="username" required><br>
    password: <input type="text" name="password" required><br>
    <input type="submit" value="signup">
</form>"""

@app.route('/admin/_login', methods=['POST'])
def api_admin_login():
    db = shelve.open('databases/users/admindata')
    username = str(request.form.get('username'))
    password = str(request.form.get('password')) 
    if username in db:
        data = db[username]
        userpass = data[0]
        if password == userpass:
            db.close()
            session['admin_username'] = username
            session['admin_login_token'] = data[1]
            return redirect(url_for('admin_panel'))
    
    db.close()
    return "login info incorrect"

@app.route("/admin")
def admin_panel():
    if 'admin_username' not in session or 'admin_login_token' not in session:
        return redirect(url_for('admin_login'))

    username = session['admin_username']
    login_token = session['admin_login_token']
    db = shelve.open('databases/users/admindata')
    if username in db:
        data = db[username]
        if login_token == data[1]:
            db.close()
            return f'logged in as {username} (admin)<form method="POST" action="/admin/logout"><input type="submit" value="Logout"></form><br><br><form method="POST" action="/admin/delete_account"><input type="checkbox" required>Check this and click button below to delete account<br><input type="submit" value="Delete account">'
    
    db.close()
    return redirect(url_for('admin_login'))

@app.route("/admin/delete_account", methods=["POST"])
def admin_delete_account():
    if 'admin_username' not in session or 'admin_login_token' not in session:
        return redirect(url_for('admin_login'))

    username = session['admin_username']
    login_token = session['admin_login_token']
    db = shelve.open('databases/users/admindata')
    if username in db:
        data = db[username]
        if login_token == data[1]:
            del db[username]
            db.close()
            session.pop('admin_username', None)
            session.pop('admin_login_token', None)
            return redirect(url_for('admin'))

    db.close()
    return redirect(url_for('admin_login'))

@app.route('/admin/logout', methods=["POST"])
def admin_logout():
    session.pop('admin_username', None)
    session.pop('admin_login_token', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)