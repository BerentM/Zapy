import json

import flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'super tajne haslo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/zapy.db'

db = SQLAlchemy(app)

from zapy import routes