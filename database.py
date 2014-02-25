from flask.ext.sqlalchemy import SQLAlchemy
from application import app
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'tmp', 'database.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH

db = SQLAlchemy(app)