from app import app

@app.route('/')
@app.route('/index')
def index():
	return "bridge - a parent-teacher web app" 
