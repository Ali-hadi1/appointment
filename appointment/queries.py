from appointment import db
from appointment.models import User, DoctorInfo, Schedule


def get_all_confirmed_doctors():
    return db.session.query(User.id, User.name, User.lastname, User.email, DoctorInfo.degree, DoctorInfo.specialty)\
              .join(User, User.id == DoctorInfo.user_id).filter(DoctorInfo.valid == True).all()


def get_all_requested_doctors():
    return db.session.query(User.id, User.name, User.lastname,User.email, User.date_of_birth, DoctorInfo.degree,
                            DoctorInfo.specialty, User.gender, DoctorInfo.valid)\
                            .join(User, User.id == DoctorInfo.user_id).filter(DoctorInfo.valid == False).all()


def get_all_doctors_has_schedule():
    # return db.session.query(User).join(Schedule, Schedule.doctor_id == User.id).group_by(User.id).all()
    return db.session.query(User).join(DoctorInfo, DoctorInfo.user_id==User.id).filter(DoctorInfo.valid == True).all()
