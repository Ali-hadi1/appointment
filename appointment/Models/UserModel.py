from appointment import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    address = db.Column(db.Text , nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date(), default = datetime.now().date())
    role = db.Column(db.Integer, nullable=False, default=3)
    gender = db.Column(db.Boolean, default=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    doctorinfo = db.relationship('DoctorInfo', backref='User', cascade="all, delete", uselist=False, lazy=True)
    schedule = db.relationship('Schedule', backref='User', lazy=True)
    appointment = db.relationship('Appointment', backref='User', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}', '{self.lastname}', '{self.address}', '{self.phone}',"\
               f"'{self.date_of_birth}', '{self.gender}', '{self.role}', '{self.username}')"

    def __init__(self, name, lastname, username, email, address, phone, dob, role, gender, password):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.email = email
        self.address = address
        self.phone = phone
        self.date_of_birth = dob
        self.role = role
        self.gender = gender
        self.password = password
        db.session.add(self)
        db.session.commit()

    def update_user(self, name, lastname, username, email, address, phone, dob, gender, role):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.email = email
        self.address = address
        self.phone = phone
        self.date_of_birth = dob
        self.gender = gender
        self.role = role
        db.session.commit()
        return self

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
        return True
