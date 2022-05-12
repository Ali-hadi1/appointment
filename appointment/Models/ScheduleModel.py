from appointment import db
from datetime import datetime

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
