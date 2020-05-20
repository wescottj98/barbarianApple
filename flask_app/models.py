from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
import pyotp

import io
import base64

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

def images(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()
    otp_secret = db.StringField(required=True, min_length=16, max_length=16, default=pyotp.random_base32())
    todo_count = db.IntField(require=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class ToDo(db.Document):
    owner = db.ReferenceField(User, required=True)
    # id = db.ObjectIdField(default=bson.ObjectId, primary_key=True)
    content = db.StringField(required=True, min_length=1, max_length=500)



