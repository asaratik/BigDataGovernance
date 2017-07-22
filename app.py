from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory, url_for
from jinja2 import Template
import os

app = Flask(__name__)

users = ['USER']
drivers = ['ADMIN']

app.secret_key = os.urandom(12)

app.config.update(
    DEBUG = True,
)

def login_required(f):
    @wraps(f)
    def login_ann(*args, **kwargs):
        if 'logged_in' in session and not session['logged_in']:
            return login_page()
        elif 'logged_in' not in session:
            return login_page()
        return f(*args, **kwargs)
    return login_ann

def login_page():
    return render_template('login.html')

@app.route('/', methods=['GET'])
@login_required
def index():
    if 'username' in session and session['username'] in users:
        return render_template("index.html")
    elif 'username' in session:
        return render_template("index_admin.html")

@app.route('/login', methods=['GET'])
@login_required
def login_get():
    if 'username' in session and session['username'] in users:
        return render_template("index.html")
    elif 'username' in session:
        return render_template("index_admin.html")

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    return login_page()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['username'].upper() in users and request.form['password'] == 'password':
        session['user'] = request.form['username']
        session['logged_in'] = True
        return render_template("index.html")
    elif request.form['username'].upper() in drivers and request.form['password'] == 'password':
        session['user'] = request.form['username']
        session['logged_in'] = True
        return render_template("index_admin.html")    
    flash('Error! The credentials are not valid, please verify!')
    return login_page()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)