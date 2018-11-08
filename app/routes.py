from flask import render_template, flash, redirect, url_for, request
from app import app, db, images
from app.forms import LoginForm, SignupForm, PostForm, ProfileEditorForm, MessageForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Message
from werkzeug.urls import url_parse
from datetime import datetime

#Index view function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        filename = images.save(request.files['image'])
        url = images.url(filename)
        post = Post(image_filename=filename, image_url=url, body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted!', 'success')
        return redirect(url_for('index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts)

#Login view function
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password', 'danger')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Log in', form=form)

#Logout view function
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

#Signup view function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = SignupForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you have signed up for Bridge!', 'success')
		return redirect(url_for('login'))
	return render_template('signup.html', title='Sign Up', form=form)

#User profile view function
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = user.posts.order_by(Post.timestamp.desc()).all()
	form = MessageForm()
	if form.validate_on_submit():
		msg = Message(sender = current_user, recipient = user, body = form.message.data)
		db.session.add(msg)
		db.session.commit()
		flash('Your message has been successfully sent!', 'success')
	return render_template('user.html', title=username, user=user, posts=posts, form=form, recipient=username)

#Profile editor view function
@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = ProfileEditorForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.gender = form.gender.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Changes saved.', 'success')
        return redirect(url_for('user', username = current_user.username))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone_number.data = current_user.phone_number
        form.date_of_birth.data = current_user.date_of_birth
        form.gender.data = current_user.gender
        form.about.data = current_user.about
    return render_template('editprofile.html', title='Edit Profile', form=form)

#Messages view function
@app.route('/messages')
@login_required
def messages():
	current_user.last_message_read_time = datetime.utcnow()
	db.session.commit()
	messages = current_user.messages_received.order_by(Message.timestamp.desc())
	return render_template('messages.html', title = 'Messages', messages = messages)
