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
    doctorinfo = db.relationship('DoctorInfo', backref='User', lazy=True )
    schedule = db.relationship('Schedule', backref='User', lazy=True)
    appointment = db.relationship('Appointment', backref='User', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}', '{self.lastname}', '{self.address}', '{self.phone}', '{self.date_of_birth}', '{self.gender}', '{self.role}')"

class DoctorInfo(db.Model):
    __tablename__='DoctorInfo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    degree = db.Column(db.String(40), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    valid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"DoctorInfo('{self.id}', '{self.user_id}', '{self.degree}', '{self.specialty}, '{self.valid}')"

class Schedule(db.Model):
    __tablename__='Schedule'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.Date(), default = datetime.now().date())
    end_date = db.Column(db.Date(), default = datetime.now().date())
    appointment = db.relationship('Appointment', backref='Schedule', lazy=True)


    def __repr__(self):
        return f"Schedule('{self.id}', '{self.doctor_id}', '{self.start_date}', '{self.end_date})"

class Appointment(db.Model):
    __tablename__='Appointment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('Schedule.id'))
    reason = db.Column(db.String(200))
    appointment_date = db.Column(db.Date(), default = datetime.now().date() )

    def __repr__(self):
        return f"Appointment('{self.id}', '{self.patient_id}', '{self.schedule_id}', '{self.reason}', '{self.appointment_date}')"

class Cash(db.Model):
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

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}', '{self.lastname}', '{self.address}', '{self.phone}', '{self.date_of_birth}', '{self.gender}', '{self.role}')"

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False)
#     lastname = db.Column(db.String(30), nullable=False)
#     email = db.Column(db.String(40), unique=True, nullable=False)
#
#     def __repr__(self):
#         return f"User('{self.name}', '{self.lastname}', '{self.email}')"
