import shelve
from flask import Flask, make_response, request
import uuid
import datetime
import hashlib

app = Flask(__name__)

def check_login(username, token):
    db = shelve.open('databases/users/userdata')
    if not username or not token:
        db.close()
        return False, False
    if username in db:
        if token == db[username][1]:
            if db[username][2] == True:
                data = db[username]
                db.close()
                return True, True, data
            data = db[username]
            db.close()
            return True, False, data
    return False, False

def short_uuid():
    # Generate a UUID
    uuid_value = uuid.uuid4()

    # Convert UUID to a bytes object
    uuid_bytes = uuid_value.bytes

    # Hash the UUID bytes using MD5 or SHA1
    hashed_uuid = hashlib.md5(uuid_bytes).digest()

    # Convert hashed UUID to a hexadecimal string
    hex_hashed_uuid = hashed_uuid.hex()

    # Truncate the hexadecimal string to 6 characters
    short_uuid = hex_hashed_uuid[:6]

    return short_uuid

admin_key = short_uuid()
print("admin key: " + admin_key + "\n")

@app.route("/")
def main():
    db = shelve.open('databases/users/userdata')
    username = request.cookies.get('un')
    login_token = request.cookies.get('LOGIN_TOKEN')
    if check_login(username, login_token) == "Error":
        return "An error has occured"
    if check_login(username, login_token)[0] == True:
        return f'logged in as {username}<form method="POST" action="/logout"><input type="submit" value="Logout"></form><br><br><form method="POST" action="/delete_account"><input type="checkbox" required>Check this and click button below to delete account<br><input type="submit" value="Delete account">'
    else:
        db.close()
        return "not logged in"
            
@app.route("/delete_account", methods=["POST"])
def delete_account():
    username = request.cookies.get('un')
    login_token = request.cookies.get('LOGIN_TOKEN')
    if check_login(username, login_token) == "Error":
        return "An error has occured"
    if check_login(username, login_token)[0] == True:
        db = shelve.open('databases/users/userdata')
        del db[username]
        db.close()
        response = make_response("<script>alert('Deleted account');</script>")
        response.delete_cookie("LOGIN_TOKEN")
        response.delete_cookie("un")
        response.headers["Location"] = "/"
        return response
    else:
        db.close()
        return "Unable to delete account: not logged in"

@app.route('/logout', methods=["POST"])
def logout():
    response = make_response("<script>alert('Logged out');</script>")
    response.delete_cookie("LOGIN_TOKEN")
    response.delete_cookie("un")
    response.headers["Location"] = "/"
    return response, 302

@app.route('/li', methods=['POST'])
def li():
    db = shelve.open('databases/users/userdata')
    username = str(request.form.get('username'))
    password = str(request.form.get('password')) 
    if not username:
        return "<script>alert('Please enter your username');history.go(-1);</script>"
    if not password:
        return "<script>alert('Please enter your password');history.go(-1);</script>"
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
            return "<script>alert('Login info incorrect');history.go(-1);</script>"
    else:
        db.close()
        return "<script>alert('Login info incorrect');history.go(-1);</script>"

@app.route('/si', methods=['POST'])
def si():
    db = shelve.open('databases/users/userdata')
    username = str(request.form.get('username'))
    data = [str(request.form.get('password')), str(uuid.uuid4()), False]
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

@app.route("/admin/signup")
def signup_form():
    return """<form method="POST" action="/admin/_signup">
    admin key <input type="text" name="admin_key" required><br>
    username <input type="text" name="username" required><br>
    password <input type="text" name="password" required><br>
    <input type="submit" value="signup">
</form>"""

@app.route('/admin/_signup', methods=['POST'])
def admmin_signup():
    db = shelve.open('databases/users/userdata')
    admin_login_key = str(request.form.get('admin_key'))
    username = str(request.form.get('username'))
    data = [str(request.form.get('password')), str(uuid.uuid4()), True]
    if not admin_login_key == admin_key:
        return "<script>alert('Admin info incorrect');history.go(-1);</script>"
    if username in db:
        db.close()
        return "<script>alert('Account already exists');history.go(-1);</script>"
    else:
        db[username] = data
        response = make_response(f"Created account<br>{username}<br>{str(data)}")
        expiration = datetime.datetime.now() + datetime.timedelta(days=365 * 10)
        response.set_cookie('LOGIN_TOKEN', data[1], expires=expiration)
        response.set_cookie('un', username, expires=expiration)
        response.headers["Location"] = "/admin/panel"
        db.close()
        return response, 302
    
@app.route("/admin")
def admin():
    return """<form method="POST" action="/admin/login">
    username <input type="text" name="username" required><br>
    password<input type="text" name="password" required><br>
    <input type="submit" value="signup">
</form>"""
    
@app.route("/admin/panel")
def panel():
    username = request.cookies.get('un')
    login_token = request.cookies.get('LOGIN_TOKEN')
    if check_login(username, login_token) == "Error":
        return "An error has occured<br>Are you logged in?"
    if check_login(username, login_token)[1] == True:
        db = shelve.open('databases/users/userdata')
        all_values = []
        all_values.append("users:")
        for key, value in db.items():
            delete_button = ''
            if key != username:
                delete_button = f'<form method="POST" action="/admin/delete_others"><input type="text" name="admin_key" value="{login_token}" hidden><input name="username" type="text" value="{key}" hidden><input type="submit" value="Delete account"></form>'
            all_values.append(f'{key}: {value} {delete_button}')
        db.close()   
        accounts = '<br>'.join(all_values)
        return f"""Logged in as {username}
                   <form method="POST" action="/logout">
                       <input type="submit" value="Logout">
                   </form>
                   {accounts}"""
    else:
        return "Invalid permissions<script>alert('Invalid permissions');history.go(-1);</script>"

@app.route("/admin/delete_others", methods=["POST"])
def admin_delete_other_account():
    db = shelve.open('databases/users/userdata')
    username = request.form.get('username')
    login_token = request.form.get('admin_key')
    if not username or not login_token:
        db.close()
        return "Invalid permissions<script>alert('Invalid data');history.go(-1);</script>"
    else:
        if username in db:
            if login_token == request.cookies.get('LOGIN_TOKEN'):
                del db[username]
                db.close()
                response = make_response("Deleted account")
                response.headers["Location"] = "/admin/panel"
                return response, 302
            else:
                db.close()
                return "<script>alert('Admin token invalid');history.go(-1);</script>"
        else:
            db.close()
            return "Invalid permissions<script>alert('Invalid data');history.go(-1);</script>"
            
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)