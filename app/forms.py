#Import python classes for web forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

#Login form class with objects created for each of the fields: description of field (1st argument)
#and validators with DataRequired() to check for empty input (2nd argument)
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Log in') 
