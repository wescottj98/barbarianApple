from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError)


from ..models import User


class CreateTodoForm(FlaskForm):
    task = StringField("Task", validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField("Create")

class UpdateTodoForm(FlaskForm):
    task = StringField("Update Content")
    submit = SubmitField("Confirm")

class ShareTodoForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    submit = SubmitField("Share")