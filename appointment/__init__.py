from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
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

app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = 'b89fc38e109879'
app.config['MAIL_PASSWORD'] = 'ae3d22d7b5c5ab'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

from appointment import routes
from appointment.Models.UserModel import User

base_dir = os.path.join(os.path.abspath(os.curdir), 'appointment')
files_in_base_dir = os.listdir(base_dir)
if 'site.db' not in files_in_base_dir:
    db.create_all()
    User('hadi', 'adelzada', 'hadi', 'admin@gmail.com', 'Kabul, Afghanistan', '0784747433', datetime(1999, 4, 3).date(),
        1, True, bcrypt.generate_password_hash("hadi").decode('utf-8'))
