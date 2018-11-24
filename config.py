import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Configuration options for Flask
class Config(object):
	SECRET_KEY = 'soen341flaskapp'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Uploads
	UPLOADS_DEFAULT_DEST = basedir + '/static/img/'

	UPLOADED_IMAGES_DEST = basedir + '/static/img/'
