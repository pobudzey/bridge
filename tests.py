import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):

	#Creates an in-memory database for testing purposes	
	def setUp(self):
		db.create_all()
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		self.app = app.test_client()
		self.app.testing = True 
	
	#Deletes the in-memory database
	def tearDown(self):
		db.session.remove()
		db.drop_all()
	
	#Password hashing test
	def test_password_hashing(self):
		u = User(username = 'maxim')
		u.set_password('goodpassword')
		self.assertFalse(u.check_password('wrongpassword'))
		self.assertTrue(u.check_password('goodpassword'))

	#Login functionality test
	def test_login(self):
		response = self.app.post('/login', data=dict(
			    username='Marct', password='12qwaszx'), follow_redirects=True)

	#Logout functionality test	
	def test_logout(self):
	    response = self.app.get('/logout', follow_redirects=True)

	#Signup page test
	def test_signup(self):
		response = self.app.post('/signup', data = dict(
				username='Marc', password='gertrecw', password2='gertrecw', 
				email='email@email.com'), follow_redirects=True)

if __name__ == '__main__':
	unittest.main()
