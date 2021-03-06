# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail
from flask_talisman import Talisman
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

import os
from datetime import datetime

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
  'retryWrites': 'false',
  'host': os.environ.get('MONGODB_URI')
}

app.config['SECRET_KEY'] = os.environ.get('CSRF_KEY')

# mongo = PyMongo(app)
db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
bcrypt = Bcrypt(app)

#flask-mail
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)

mail = Mail(app)

from flask_app.main.routes import main
from flask_app.users.routes import users

app.register_blueprint(main)
app.register_blueprint(users)

csp = {
    'default-src':'\'self\'',
    'script-src': [
      '\'self\'',
      'https://stackpath.bootstrapcdn.com',
      'https://code.jquery.com',
      'https://cdn.jsdelivr.net',
      '\'unsafe-inline\'' # Allow inline JS to modify our frontend and make interactive
    ],
    'style-src': [
      '\'self\'',
      'https://stackpath.bootstrapcdn.com',
    ],
    'font-src': [
      '\'self\'',
      'data:'
    ],
    'img-src': [
      '\'self\'',
      'data:'
    ]
}

Talisman(app, content_security_policy = csp)

@app.after_request
def apply_security(response):
  response.headers['Content-Security-Policy'] = "default src 'self'"
  response.headers['Strict-Transport-Secutiy'] = "default src 'self'"
  response.headers['X-Content-Type-Options'] = "nosniff"
  response.headers['X-Frame-Options'] = "default src 'self'"
  response.headers['X-XSS-Protection'] = "default src 'self'"

  return response