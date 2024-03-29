from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):
    '''Form for registering a user'''
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=30)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[InputRequired()])
    
class LoginForm(FlaskForm):
    '''Form for logging in a user'''
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    '''Form for adding feedback'''
    title = StringField('Title', validators=[InputRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', validators=[InputRequired()])
    