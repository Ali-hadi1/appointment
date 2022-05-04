from flask import render_template, redirect, url_for, request, flash
from appointment import db
from appointment.forms import DoctorInfoForm, CreateSchedule, MakeAppointment, UpdateAccount, EditUserInfo
from appointment.models import DoctorInfo, User, Schedule, Appointment
from flask_login import current_user
from sqlalchemy import and_
from datetime import datetime

base_url = 'http://127.0.0.1:9000'


def create_doctor_info(id):
    form = DoctorInfoForm()
    if form.validate_on_submit():
        DoctorInfo(id, form.degree.data, form.specialty.data)
        flash("Your Info submitted successfully wait for conformation!", 'info')
        return redirect(url_for('home'))
    return render_template('doctor_info_form.html', form=form)


def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if current_user.id == id:
        flash("Ooops, unable to delete your self!", "warning")
        redirect(url_for("users"))
    user.delete_user()
    return redirect(url_for('users'))


def create_schedule():
    form = CreateSchedule()
    if form.validate_on_submit():
        Schedule(form.name.data, current_user.id, form.start_date.data, form.end_date.data, form.description.data)
        return render_template('schedule.html', form=form, schedules=current_user.schedule)
    return render_template("schedule.html", form=form, schedules=current_user.schedule)


def view_doctor_schedule(id):
    doctor = User.query.filter_by(id=id).first()
    return render_template("view_schedules.html", schedules=doctor.schedule)


def patient_create_appointment(id):
    form = MakeAppointment()
    form.schedule_id.data = id
    appointing_schedule = Schedule.query.filter_by(id=id).first()
    if form.validate_on_submit():
        incoming_date_exist = db.session.query(Appointment)\
            .filter(and_(Appointment.schedule_id == id,
                         Appointment.appointment_date == form.date.data)).all()
        if incoming_date_exist:
            flash("this date booked before Please choose a different one!", "info")
            return redirect(url_for('patientAppointment', id=id))
        Appointment(current_user.id, form.schedule_id.data, form.reason.data, form.date.data)
        doctor_id = Schedule.query.filter_by(id=id).first()
        return redirect(url_for('viewSchedule', id=doctor_id.doctor_id))
    return render_template('patientAppointment.html', form=form, seleted_schedule=appointing_schedule,
                           today=datetime.now().date())


def admin_create_doctor_schedule(id):
    doctor = User.query.filter_by(id=id).first()
    form = CreateSchedule()
    if form.validate_on_submit():
        Schedule(form.name.data, doctor.id, form.start_date.data, form.end_date.data, form.description.data)
        return redirect(url_for('get_and_create_doctor_schedule', id=doctor.id))
    return render_template("adminPanel/doctor_schedule_list.html", schedules=doctor.schedule, form=form)


def delete_doctor_schedule(id):
    schedule_delete = Schedule.query.filter_by(id=id).first()
    id = schedule_delete.doctor_id
    schedule_delete.delete_doctor_schedule()
    if request.url == base_url+"/schedule":
        return redirect(url_for('schedule'))
    return redirect(url_for('get_and_create_doctor_schedule', id=id))


def edit_doctor_schedule(id):
    form = CreateSchedule()
    doctor_schedule = Schedule.query.filter_by(id=id).first()
    if form.validate_on_submit():
        doctor_schedule.update_doctor_schedule(form.name.data, form.start_date.data, form.end_date.data,
                                               form.description.data)
        flash("Schedule successfully edited", 'info')
        if request.url == base_url + '/admin/doctors/schedules/edit/' + str(id):
            return redirect(url_for('get_and_create_doctor_schedule', id=doctor_schedule.doctor_id))
        return redirect(url_for('schedule'))
    form.description.data = doctor_schedule.description
    if request.url == base_url + '/admin/doctors/schedules/edit/' + str(id):
        return render_template('adminPanel/doctor_schedule_edit.html', form=form, id=doctor_schedule.doctor_id,
                               schedule=doctor_schedule)
    return render_template('edit_schedule.html', form=form, id=doctor_schedule.doctor_id, schedule=doctor_schedule)


def appointed_patient_on_a_schedule(id):
    patient_list = db.session.query(User.name, User.lastname, User.phone, User.gender, Appointment.reason, Appointment.appointment_date)\
                    .join(Appointment, User.id == Appointment.patient_id).filter(Appointment.schedule_id == id).all()
    return render_template('appointed_patients.html', patients=patient_list)


def all_appointed_patient_list():
    all_appointed_patient = db.session.query(User.name, User.lastname, User.phone, User.gender,
                         Appointment.reason, Appointment.id, Appointment.appointment_date)\
                         .join(Appointment, User.id == Appointment.patient_id).all()
    return render_template('adminPanel/appointment_list.html', patients=all_appointed_patient)


def get_user_info(id):
    form = EditUserInfo()
    user_info = User.query.filter_by(id=id).first()
    return render_template('user_info.html', user=user_info, form=form)


def delete_an_appointment(id):
    selected_appointment = Appointment.query.filter_by(id=id).first()
    selected_appointment.delete_appointment()
    return redirect(url_for('appointed_patient_list'))


def current_user_profile():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.update_user(form.name.data, form.lastname.data, form.username.data, form.email.data,
                                 form.address.data, form.phone.data, form.date_of_birth.data, current_user.gender)
        flash('Your account Updated Successfully', 'success')
        if request.url == base_url + "/admin/profile":
            return redirect(url_for('admin_profile'))
        return redirect(url_for('profile'))
    if request.url == base_url + "/admin/profile":
        return render_template("adminPanel/admin_profile.html", form=form)
    return render_template('profile.html', form=form)


def get_users_with_pagenation():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=7)
    return render_template("/usersList.html", users=users)