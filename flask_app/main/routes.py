from flask import render_template, request, redirect, url_for, flash, send_file, Blueprint
from flask_mongoengine import MongoEngine
from flask_mail import Message
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from PIL import Image

# stdlib
from datetime import datetime
import io
import base64

# local
from .. import app, bcrypt, mail
from .forms import (CreateTodoForm, UpdateTodoForm,
                             ShareTodoForm)
from ..models import User, load_user, ToDo, images
from ..utils import current_time

main = Blueprint("main", __name__)

""" ************ View functions ************ """
@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    return render_template('index.html')

@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/todos/delete/<todo_id>', methods=['POST'])
def deleteTodo(todo_id):
    todo = ToDo.objects(id=todo_id).first()
    if todo is None:
        flash('Todo not found to delete')
    else:
        todo.delete()
        User.objects(id=current_user.id).update_one(dec__todo_count=1)

    return redirect(url_for('main.todo'))

@main.route('/todos/update/<todo_id>', methods=['POST'])
def updateTodo(todo_id):
    updateTodo_form = UpdateTodoForm()

    if updateTodo_form.validate_on_submit():

        update = ToDo.objects(id=todo_id).update_one(content=updateTodo_form.task.data)
        
        if update != True:
            flash('Todo not found to update')

    return redirect(url_for('main.todo'))


@main.route('/todos/share/<todo_id>', methods=['POST'])
def shareTodo(todo_id):
    share_form = ShareTodoForm()

    if share_form.validate_on_submit():

        todo = ToDo.objects(id=todo_id).first()

        if todo is None:
            flash('Todo not found to share')
        else:
            msg = Message(subject=current_user.username + " has shared a Todo with you!",
                        sender="Todo App",
                        recipients=[share_form.email.data],
                        body="Todo: " + todo.content)
            
            mail.send(msg)


    return redirect(url_for('main.todo'))

@main.route('/user/<username>')
def user_detail(username):
    user = User.objects(username=username).first()

    if user is None:
        flash('User not found')
        return render_template('user_detail.html'), 404
        
    image = images(username)

    return render_template('user_detail.html', user=user,  image=image)


@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    top_users = User.objects.order_by('-todo_count')

    return render_template('home.html', topusers = top_users[:10])

@main.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    createTodo_form = CreateTodoForm()
    updateTodo_form = UpdateTodoForm()
    share_form = ShareTodoForm()

    current_user_to_do_list = ToDo.objects(owner=load_user(current_user.username))

    if createTodo_form.validate_on_submit():
        toDo = ToDo(
            owner = load_user(current_user.username),
            content = createTodo_form.task.data
        )
        toDo.save()

        User.objects(id=current_user.id).update_one(inc__todo_count=1)

        return redirect(url_for('main.todo'))


    return render_template('todo.html', createTodo_form=createTodo_form, updateTodo_form=updateTodo_form, share_form=share_form, current_user_to_do_list=current_user_to_do_list)
