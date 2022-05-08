from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '1caae790185db9529f000ce7b22d83ab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from appointment import routes
from appointment.models import User

base_dir = os.path.join(os.path.abspath(os.curdir), 'appointment')
files_in_base_dir = os.listdir(base_dir)
if 'site.db' not in files_in_base_dir:
    db.create_all()

