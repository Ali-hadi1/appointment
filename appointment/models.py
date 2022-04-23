from appointment import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    address = db.Column(db.Text , nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    date_of_birth = db.Column(db.DateTime(), default = datetime.utcnow )
    role = db.Column(db.Integer, nullable=False, default=3)
    gender = db.Column(db.Boolean, default=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    doctorinfo = db.relationship('DoctorInfo', backref='User', lazy=True )

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}', '{self.lastname}', '{self.address}', '{self.phone}', '{self.date_of_birth}', '{self.gender}', '{self.role}')"

class DoctorInfo(db.Model):
    __tablename__='DoctorInfo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    degree = db.Column(db.String(40), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"DoctorInfo('{self.id}', '{self.user_id}', '{self.degree}', '{self.specialty}')"


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False)
#     lastname = db.Column(db.String(30), nullable=False)
#     email = db.Column(db.String(40), unique=True, nullable=False)
#
#     def __repr__(self):
#         return f"User('{self.name}', '{self.lastname}', '{self.email}')"
