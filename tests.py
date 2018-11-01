import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):

	#Creates an in-memory database for testing purposes	
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()
	
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

	#Login behaviour test
	def login(self, username, password):
		r = self.app.post('/login', data=dict(username='marc', 
		password='asdfcxz'), follow_redirects=True)
		self.assertIn('Log in successful', r.data)
		self.assertTrue()

	#Logout behaviour test
	def logout(self):
		r = self.app.post('/login', data=dict(username='marc', 
		password='asdfcxz'), follow_redirects=True)
		self.assertIn('Log out successful', r.data)


if __name__ == '__main__':
	unittest.main()
