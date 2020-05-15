from flask import render_template, request, redirect, url_for, flash, Response, send_file, Blueprint
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from PIL import Image

# stdlib
from datetime import datetime
import io
import base64

# local
from .. import app, bcrypt
from .forms import (RegistrationForm, LoginForm,
                             UpdateUsernameForm, UpdateProfilePicForm)
from ..models import User, Review, load_user
from ..utils import current_time

main = Blueprint("main", __name__)

""" ************ View functions ************ """
@main.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html', form=form)
'''
@main.route('/search-results/<query>', methods=['GET'])
def query_results(query):
    results = client.search(query)

    if type(results) == dict:
        return render_template('query.html', error_msg=results['Error'])
    
    return render_template('query.html', results=results)

@main.route('/toDoList/<toDo_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    result = client.retrieve_movie_by_id(movie_id)

    if type(result) == dict:
        return render_template('movie_detail.html', error_msg=result['Error'])

    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=load_user(current_user.username), 
            content=form.text.data, 
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title
        )

        review.save()

        return redirect(request.path)

    reviews_m = Review.objects(imdb_id=movie_id)

    reviews = []
    for r in reviews_m:
        reviews.append({
            'date': r.date,
            'username': r.commenter.username,
            'content': r.content,
            'image': images(r.commenter.username)
        })


    return render_template('movie_detail.html', form=form, movie=result, reviews=reviews)
'''
@main.route('/user/<username>')
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    image = images(username)

    return render_template('user_detail.html', username=username, reviews=reviews, image=image)

# @main.route('/images/<username>.png')
def images(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image
