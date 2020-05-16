# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
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
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)


from flask_app.main.routes import main
from flask_app.users.routes import users

app.register_blueprint(main)
app.register_blueprint(users)