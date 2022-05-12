from appointment import db

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
