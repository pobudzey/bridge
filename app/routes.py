from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home page')

@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', title='Log in', form=form)
