from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

#Login form
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Log in')

#Signup form
class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Register')
	
	#Method that checks if the entered username is already in the database
	def validate_user(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('This username isn\'t available. Please try another one.')
	
	#Method that checks if the entered email is used by an existing username in the database
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('This email address is in use by an existing account. Please use another one.') 

#Form for posts
class PostForm(FlaskForm):
    post = TextAreaField('Say something!', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
