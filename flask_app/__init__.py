# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for, response
from flask_mail import Mail
from flask_talisman import Talisman
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime


app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/second_database"
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/to_do_list_app'
app.config['SECRET_KEY'] = b'\x020;yr\x91\x11\xbe"\x9d\xc1\x14\x91\xadf\xec'

# mongo = PyMongo(app)
db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
bcrypt = Bcrypt(app)

#flask-mail
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SENDER'] = os.environ.get('MAIL_SENDER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')

mail = Mail(app)

from flask_app.main.routes import main
from flask_app.users.routes import users

app.register_blueprint(main)
app.register_blueprint(users)

csp = {
    'default-src':'\'self\''
}

Talisman(app, content_security_policy = csp)


response.headers['Content-Security-Policy'] = "default src 'self'"
response.headers['Strict-Transport-Secutiy'] = "default src 'self'"
response.headers['X-Content-Type-Options'] = "nosniff"
response.headers['X-Frame-Options'] = "default src 'self'"
response.headers['X-XSS-Protection'] = "default src 'self'"