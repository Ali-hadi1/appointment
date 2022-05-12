from appointment import db
from datetime import datetime


class Appointment(db.Model):
    __tablename__='Appointment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('Schedule.id'))
    reason = db.Column(db.String(200))
    state = db.Column(db.String(20), default='drift')
    appointment_date = db.Column(db.Date(), default = datetime.now().date())

    def __repr__(self):
        return f"Appointment('{self.id}', '{self.patient_id}', '{self.schedule_id}'," \
               f"'{self.reason}', '{self.appointment_date}', '{self.state}')"

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
    
    def change_appointment_state(self, str):
        self.state = str
        db.session.commit()