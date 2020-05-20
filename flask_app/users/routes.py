from flask import render_template, request, redirect, url_for, flash, send_file, Blueprint, session
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from PIL import Image
#2FA/TFA
import pyotp
import qrcode
import qrcode.image.svg as svg
from io import BytesIO

# stdlib
from datetime import datetime

# local
from .. import app, bcrypt
from .forms import (RegistrationForm, LoginForm,
                             UpdateUsernameForm, UpdateProfilePicForm)
from ..models import User, load_user, images
from ..utils import current_time

users = Blueprint("users", __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user = User(username=form.username.data, email=form.email.data, password=hashed, todo_count=0)
        user.save()
        session['new_username'] = user.username

        return redirect(url_for('users.tfa'))

    return render_template('register.html', title='Register', form=form)

@users.route("/qr_code")
def qr_code():
    if 'new_username' not in session:
        return redirect(url_for('main.index'))
    
    user = User.objects(username=session['new_username']).first()
    session.pop('new_username')

    uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(name=user.username, issuer_name='ToDoList-App-2FA-GP517')
    img = qrcode.make(uri, image_factory=svg.SvgPathImage)
    stream = BytesIO()
    img.save(stream)

    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return stream.getvalue(), headers

@users.route("/tfa")
def tfa():
    if 'new_username' not in session:
        return redirect(url_for('main.index'))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return render_template('2fa.html'), headers


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # return redirect(url_for('users.account'))
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Check your username and/or password')
            return redirect(url_for('users.login'))

    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    username_form = UpdateUsernameForm()
    profile_pic_form = UpdateProfilePicForm()

    print(username_form.submit.data)
    print(profile_pic_form.submit.data)
    # We have to make sure the form was actually submitted before validating since we have 2 forms on one page
    if username_form.submit.data and username_form.validate_on_submit():
        current_user.modify(username=username_form.username.data)
        current_user.save()
        login_user(current_user)

        return redirect(url_for('users.account'))

    if profile_pic_form.submit.data and profile_pic_form.validate_on_submit():
        img = profile_pic_form.propic.data
        filename = secure_filename(img.filename)

        if current_user.profile_pic.get() is None:
            current_user.profile_pic.put(img.stream, content_type='images/png')
        else:
            current_user.profile_pic.replace(img.stream, content_type='images/png')
        current_user.save()

        return redirect(url_for('users.account'))

    image = images(current_user.username)

    return render_template("account.html", title="Account", username_form=username_form, profile_pic_form=profile_pic_form, image=image)
