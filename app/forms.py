from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    firstname = StringField('First Name', [validators.Length(min=3, max=20)])
    lastname = StringField('Last Name', [validators.Length(min=3, max=20)])
    username = StringField('Username', [validators.Length(min=6, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password must match')
        ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Sign up')
    
