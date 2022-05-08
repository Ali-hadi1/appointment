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


class DoctorInfo(db.Model):
    __tablename__='DoctorInfo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    degree = db.Column(db.String(40), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    valid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"DoctorInfo('{self.id}', '{self.user_id}', '{self.degree}', '{self.specialty}, '{self.valid}')"

    def __init__(self, user_id, degree, specialty):
        self.user_id = user_id
        self.degree = degree
        self.specialty = specialty
        db.session.add(self)
        db.session.commit()

    def update_doctor_info(self, degree, specialty):
        self.degree = degree
        self.specialty = specialty
        db.session.commit()
        return self


class Schedule(db.Model):
    __tablename__='Schedule'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.Date(), default = datetime.now().date())
    end_date = db.Column(db.Date(), default = datetime.now().date())
    description = db.Column(db.Text())
    appointment = db.relationship('Appointment', backref='Schedule', lazy=True)

    def __repr__(self):
        return f"Schedule('{self.id}', '{self.name}' '{self.doctor_id}', '{self.start_date}', '{self.end_date}," \
               f" '{self.description}')"

    def __init__(self, name, doctor_id, start_date, end_date, description):
        self.name = name
        self.doctor_id = doctor_id
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        db.session.add(self)
        db.session.commit()

    def update_doctor_schedule(self, name, start_date, end_date, description):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        db.session.commit()
        return self

    def delete_doctor_schedule(self):
        db.session.delete(self)
        db.session.commit()
        return True


class Appointment(db.Model):
    __tablename__='Appointment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('Schedule.id'))
    reason = db.Column(db.String(200))
    appointment_date = db.Column(db.Date(), default = datetime.now().date() )

    def __repr__(self):
        return f"Appointment('{self.id}', '{self.patient_id}', '{self.schedule_id}'," \
               f"'{self.reason}', '{self.appointment_date}')"

    def __init__(self, patient_id, schedule_id, reason, appointment_date):
        self.patient_id = patient_id
        self.schedule_id = schedule_id
        self.reason = reason
        self.appointment_date = appointment_date
        db.session.add(self)
        db.session.commit()

    def update_appointment(self, reason, appointment_date):
        self.reason = reason
        self.appointment_date = appointment_date
        db.session.commit()
        return self

    def delete_appointment(self):
        db.session.delete(self)
        db.session.commit()
        return True


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
        return f"User('{self.id}', '{self.name}', '{self.email}', '{self.lastname}'," \
               f"'{self.address}', '{self.phone}', '{self.date_of_birth}', '{self.gender}', '{self.role}')"

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False)
#     lastname = db.Column(db.String(30), nullable=False)
#     email = db.Column(db.String(40), unique=True, nullable=False)
#
#     def __repr__(self):
#         return f"User('{self.name}', '{self.lastname}', '{self.email}')"
