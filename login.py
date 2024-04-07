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
    db = shelve.open('databases/users/admindata')
    admin_login_key = str(request.form.get('admin_key'))
    username = str(request.form.get('username'))
    data = [str(request.form.get('password')), str(uuid.uuid4())]
    print(username)
    print(data[0])
    if not admin_login_key == "3gr978":
        return "Admin key incorrect"
    if username in db:
        db.close()
        return "Account already exists"
    else:
        db[username] = data
        response = make_response(f"Created account<br>{username}<br>{str(data)}")
        expiration = datetime.datetime.now() + datetime.timedelta(days=365 * 10)
        response.set_cookie('admin_LOGIN_TOKEN', data[1], expires=expiration)
        response.set_cookie('admin_un', username, expires=expiration)
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

@app.route('/admin/login', methods=['POST'])
def admin_login():
    db = shelve.open('databases/users/admindata')
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
            response.set_cookie('admin_LOGIN_TOKEN', data[1], expires=expiration)
            response.set_cookie('admin_un', username, expires=expiration)
            response.headers["Location"] = "/admin/panel"
            return response, 302
        else:
            return "login info incorrect"
    else:
        db.close()
        return "login info incorrect"
    
@app.route("/admin/panel")
def panel():
    db = shelve.open('databases/users/admindata')
    username = request.cookies.get('admin_un')
    login_token = request.cookies.get('admin_LOGIN_TOKEN')
    if not username or not login_token:
        return "not logged in"
    else: 
        if username in db:
            data = db[username]
            if login_token == data[1]:
                db = shelve.open('databases/users/userdata')
                all_values = []
                all_values.append("users:")
                for key, value in db.items():
                    all_values.append(f'{key}: {value} <form method="POST" action="/admin/delete_others"><input type="text" name="admin_key" value="3gr978" hidden><input name="username" type="text" value="{key}" hidden><input type="submit" value="Delete account">')
                db.close()   
                accounts = '<br>'.join(all_values)
                return f"""logged in as {username}<form method="POST" action="/logout_admin"><input type="submit" value="Logout"></form>
            {accounts}
            """
            else:
                db.close()
                return "not logged in"

@app.route('/logout_admin', methods=["POST"])
def admin_logout():
    response = make_response("Logged out")
    response.delete_cookie("admin_LOGIN_TOKEN")
    response.delete_cookie("admin_un")
    response.headers["Location"] = "/"
    return response, 302

@app.route("/admin/delete_others", methods=["POST"])
def admin_delete_other_account():
    db = shelve.open('databases/users/userdata')
    username = request.form.get('username')
    login_token = request.form.get('admin_key')
    if not username or not login_token:
        return "Unable to delete account: not logged in"
    else:
        if username in db:
            if login_token == "3gr978":
                del db[username]
                db.close()
                response = make_response("Deleted account")
                response.delete_cookie("LOGIN_TOKEN")
                response.delete_cookie("un")
                response.headers["Location"] = "/admin/panel"
                return response, 302
            else:
                db.close()
                return "Unable to delete account"
            
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)