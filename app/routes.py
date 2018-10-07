from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, SignupForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
		return redirect(url_for('index'))
	return render_template('login.html', title='Log in', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	return render_template('signup.html', title='Sign Up', form=form)
