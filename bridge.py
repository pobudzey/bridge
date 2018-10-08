from app import app, db
from app.models import User, Post

#Shell context function
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}
