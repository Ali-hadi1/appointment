from appointment import db
from flask import request
from appointment.Models.UserModel import User
from appointment.Models.DoctorInfoModel import DoctorInfo
from appointment.Models.ScheduleModel import Schedule
from appointment.Models.AppointmentModel import Appointment


def get_all_confirmed_doctors():
    return db.session.query(User.id, User.name, User.lastname, User.email, DoctorInfo.degree, DoctorInfo.specialty)\
              .join(User, User.id == DoctorInfo.user_id).filter(DoctorInfo.valid == True).all()


def get_all_requested_doctors():
    return db.session.query(User.id, User.name, User.lastname,User.email, User.date_of_birth, DoctorInfo.degree,
                            DoctorInfo.specialty, User.gender, DoctorInfo.valid)\
                            .join(User, User.id == DoctorInfo.user_id).filter(DoctorInfo.valid == False).all()


def get_all_doctors():
    page = request.args.get('page', 1, type=int)
    return db.session.query(User).join(DoctorInfo, DoctorInfo.user_id==User.id).filter(DoctorInfo.valid == True)\
                                 .paginate(page=page, per_page=7)


def get_doctor_schedule(id):
    return Schedule.query.filter(Schedule.doctor_id == id).all()


def get_user_appointment(id):
    page = request.args.get('page', 1, type=int)
    return db.session.query(User.name.label('firstname'), User.lastname, User.email, Schedule.name, Appointment.id, Appointment.appointment_date)\
            .join(Schedule, Schedule.doctor_id == User.id).join(Appointment, Schedule.id == Appointment.schedule_id)\
            .filter(Appointment.patient_id == id).paginate(page=page, per_page=8)


def get_schedule_list(id):
    page = request.args.get('page', 1, type=int)
    return Schedule.query.filter(Schedule.doctor_id==id).paginate(page=page, per_page=8)


def get_all_patients():
    return User.query.filter(User.role==3).all()

