from flask import render_template, flash, redirect, url_for, request
from app import app, db, images
from app.forms import LoginForm, SignupForm, PostForm, ProfileEditorForm, MessageForm, AddMemberForm, CreateGroupForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Message, Group, Comment
from werkzeug.urls import url_parse
from datetime import datetime

#Index view function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    form2 = CreateGroupForm()
    if form.validate_on_submit():
        if form.image.data is not None:
            filename = images.save(request.files['image'])
            url = images.url(filename)
            post = Post(body=form.post.data, author=current_user, image_filename = filename, image_url = url)
        else:
            post = Post(body = form.post.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted!', 'success')
        return redirect(url_for('index'))
    if form2.validate_on_submit():
        group = Group.query.filter_by(name = form2.name.data).first()
        if group is None:
            group = Group(name = form2.name.data, description = form2.description.data)
            db.session.add(group)
            current_user.add_to_group(group)
            db.session.commit()
            flash('Group created!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Such a group already exists. Pick another name.', 'danger')
            return redirect(url_for('index'))
    posts = Post.query.filter_by(parent_group = None).order_by(Post.timestamp.desc()).all()
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts, form2 = form2)

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
	posts = user.posts.filter_by(parent_group = None).order_by(Post.timestamp.desc()).all()
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

#Group view function
@app.route('/group/<name>', methods = ['GET', 'POST'])
@login_required
def group(name):
    group = Group.query.filter_by(name = name).first_or_404()
    posts = Post.query.filter_by(parent_group = group).order_by(Post.timestamp.desc()).all()
    form1 = PostForm()
    form2 = AddMemberForm()
    if form1.validate_on_submit():
        if form1.image.data is not None:
            filename = images.save(request.files['image'])
            url = images.url(filename)
            post = Post(body = form1.post.data, author = current_user, parent_group = group, image_filename = filename, image_url = url)
        else:
            post = Post(body = form1.post.data, author = current_user, parent_group = group)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted!', 'success')
        return redirect(url_for('group', name = group.name))
    if form2.validate_on_submit():
        user = User.query.filter_by(username = form2.member.data).first()
        if user is None:
            flash('No such user found.', 'danger')
            return redirect(url_for('group', name = group.name))
        elif user.belongs_to_group(group):
            flash(user.username + ' is already a member of this group', 'warning')
            return redirect(url_for('group', name = group.name))
        else:
            user.add_to_group(group)
            db.session.commit()
            flash('You have successfully added ' + user.username + ' to the group.', 'success')
            return redirect(url_for('group', name = group.name))
    return render_template('group.html', title = name, group = group, form1 = form1, posts = posts, form2 = form2)

#Remove member from group view function
@app.route('/remove/<username>/<groupname>')
@login_required
def remove(username, groupname):
    user = User.query.filter_by(username = username).first()
    group = Group.query.filter_by(name = groupname).first()
    user.remove_from_group(group)
    posts = Post.query.filter_by(parent_group = group).filter_by(author = user).all()
    for p in posts:
        db.session.delete(p)
    db.session.commit()
    flash('You have successfully removed ' + user.username + ' from the group.', 'success')
    return redirect(url_for('group', name = groupname))

#Like post view function
@app.route('/like/<post_id>')
@login_required
def like(post_id):
    post = Post.query.filter_by(id = post_id).first_or_404()
    if current_user.has_liked(post):
        current_user.unlike(post)
    elif not current_user.has_liked(post) and not current_user.has_disliked(post):
        current_user.like(post)
    else:
        current_user.undislike(post)
        current_user.like(post)
    db.session.commit()
    if post.parent_group:
        return redirect(url_for('group', name = post.parent_group.name))
    else:
        return redirect(url_for('index'))

#Dislike post view function
@app.route('/dislike/<post_id>')
@login_required
def dislike(post_id):
    post = Post.query.filter_by(id = post_id).first_or_404()
    if current_user.has_disliked(post):
        current_user.undislike(post)
    elif not current_user.has_disliked(post) and not current_user.has_liked(post):
        current_user.dislike(post)
    else:
        current_user.unlike(post)
        current_user.dislike(post)
    db.session.commit()
    if post.parent_group:
        return redirect(url_for('group', name = post.parent_group.name))
    else:
        return redirect(url_for('index'))

#Comment view function
@app.route('/comment/<post_id>', methods = ['GET', 'POST'])
@login_required
def comment(post_id):
    post = Post.query.filter_by(id = post_id).first_or_404()
    comment = Comment(body = request.form['comment'], author = current_user, parent_post = post)
    db.session.add(comment)
    db.session.commit()
    flash('You have successfully commented!', 'success')
    if post.parent_group:
        return redirect(url_for('group', name = post.parent_group.name))
    else:
        return redirect(url_for('index'))
