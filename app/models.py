from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#User-to-group association table
user_to_group = db.Table('user_to_group', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True), db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key = True))

#User database model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about = db.Column(db.String(140))
    messages_sent = db.relationship('Message', foreign_keys = 'Message.sender_id', backref = 'sender', lazy = 'dynamic')
    messages_received = db.relationship('Message', foreign_keys = 'Message.recipient_id', backref = 'recipient', lazy = 'dynamic')
    last_message_read_time = db.Column(db.DateTime)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    groups = db.relationship('Group', secondary = user_to_group, lazy = 'dynamic', backref = db.backref('members', lazy = 'dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
    	return User.query.get(int(id))
    
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient = self).filter(Message.timestamp > last_read_time).count()
    
    #Check if the user belongs to a group
    def belongs_to_group(self, group):
        return self.groups.filter(user_to_group.c.group_id == group.id).count() > 0

    #Add the user to a group
    def add_to_group(self, group):
        if not self.belongs_to_group(group):
            self.groups.append(group)

    #Remove the user from a group
    def remove_from_group(self, group):
        if self.belongs_to_group(group):
            self.groups.remove(group)

#Post database model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

#Message database model
class Message(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	body = db.Column(db.String(500))
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	
	def __repr__(self):
		return '<Message {}>'.format(self.body)

#Group database model
class Group(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = True, nullable = False)
    description = db.Column(db.String(250))
    posts = db.relationship('Post', backref = 'parent_group', lazy = 'dynamic')

    def __repr__(self):
        return '<Group %r>' % self.name
