from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKeyHere'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {'employee1': {'password': 'password123', 'name': 'John Doe'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    if username in users and request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for('dashboard'))
    return 'Invalid credentials'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=users[request.form['username']]['name'])

if __name__ == '__main__':
    app.run(debug=True)
