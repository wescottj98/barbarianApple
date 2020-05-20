from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
import pyotp

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


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



