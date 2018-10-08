#Import Flask class from flask package, Config class from config package, SQLAlchemy class
#from flask_sqlalchemy package and Migrate class from flask_migrate package
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
