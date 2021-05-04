import json

import flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = '4d28e498bdab65c69062da90755f0e44e7cd10d5973f1a82361397e1c377b82f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/zapy.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from zapy import routes