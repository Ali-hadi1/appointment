from appointment import bcrypt
from flask import render_template, redirect, url_for, request, flash
from appointment import db, mail
from appointment.forms import DoctorInfoForm, CreateSchedule, MakeAppointment, UpdateAccount, ChangePassword
from appointment.Models.UserModel import User
from appointment.Models.DoctorInfoModel import DoctorInfo
from appointment.Models.ScheduleModel import Schedule
from appointment.Models.AppointmentModel import Appointment
from flask_login import current_user
from sqlalchemy import and_
from datetime import datetime
from flask_mail import Message
from appointment.queries import get_schedule_list

base_url = 'http://127.0.0.1:9000'


def create_doctor_info(id):
    form = DoctorInfoForm()
    if form.validate_on_submit():
        DoctorInfo(id, form.degree.data, form.specialty.data)
        flash("Your Info submitted successfully wait for conformation!", 'info')
        flash("Confirmation Email will send to your email", 'info')
        return redirect(url_for('home'))
    return render_template('doctor_info_form.html', form=form)


def confirm_doctor_request(id):
    try: 
        doctor = User.query.filter_by(id=id).first()
        doctor_info = DoctorInfo.query.filter_by(user_id=id).first()
        msg = Message(subject="Testing mail", sender="info@test.com", recipients=[doctor.email])
        msg.body = render_template('mail_template.html', lastname=doctor.lastname)
        mail.send(msg)
        doctor_info.valid = True
        db.session.commit()
        flash('The request confirmed successfully', 'success')
    except:
        flash("something is going wrong!", 'danger')


def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if current_user.id == id:
        flash("Ooops, unable to delete your self!", "warning")
        redirect(url_for("users"))
    user.delete_user()
    if request.args.get('from'):
        return redirect(url_for('requests'))
    return redirect(url_for('users'))


def create_schedule():
    form = CreateSchedule()
    if form.validate_on_submit():
        schedules = Schedule.query.filter_by(doctor_id=current_user.id)\
            .filter((Schedule.start_date.between(form.start_date.data, form.end_date.data) | (Schedule.end_date.between(form.start_date.data, form.end_date.data)) | \
                 ((Schedule.start_date <= form.start_date.data) & (Schedule.end_date >= form.end_date.data)))).all()
        if schedules:
            flash('Schedules date Confilcted', 'warning')
            return render_template('schedule.html', form=form, schedules=get_schedule_list(current_user.id))
        if form.start_date.data <= form.end_date.data:
            Schedule(form.name.data, current_user.id, form.start_date.data, form.end_date.data, form.description.data)
            return render_template('schedule.html', form=form, schedules=get_schedule_list(current_user.id))
        flash("Please choose proper date", 'info')
        return render_template("schedule.html", form=form, schedules=get_schedule_list(current_user.id))
    current_user_schedules = get_schedule_list(current_user.id)
    return render_template("schedule.html", form=form, schedules=current_user_schedules)


def view_doctor_schedule(id):
    doctor = User.query.filter_by(id=id).first()
    if not doctor.schedule:
        flash("This doctor doesn't have any schedule!", 'info')
        return redirect(url_for('home'))
    return render_template("view_schedules.html", schedules=doctor.schedule, todaydate=datetime.now().date())


def patient_create_appointment(id):
    form = MakeAppointment()
    form.schedule_id.data = id
    appointing_schedule = Schedule.query.filter_by(id=id).first()
    if current_user.id == appointing_schedule.doctor_id:
        flash("You can't make appointment in your schedules", 'warning')
        return redirect(url_for('viewSchedule', id=appointing_schedule.doctor_id))
    if form.validate_on_submit():
        if form.date.data > appointing_schedule.end_date:
            flash("This date isn't in range of this schedule!", 'warning')
            return redirect(url_for('patientAppointment', id=id))
        incoming_date_exist = db.session.query(Appointment)\
            .filter(and_(Appointment.schedule_id == id,
                         Appointment.appointment_date == form.date.data)).order_by(Appointment.id.desc()).first()
        if incoming_date_exist and  incoming_date_exist.state != 'cancel':
            flash("this date booked before Please choose a different one!", "info")
            return redirect(url_for('patientAppointment', id=id))
        Appointment(current_user.id, form.schedule_id.data, form.reason.data, form.date.data)
        flash('your appoitment submited successfuly on ' + str(form.date.data), 'success')
        return redirect(url_for('viewSchedule', id=appointing_schedule.doctor_id))
    return render_template('patientAppointment.html', form=form, seleted_schedule=appointing_schedule,
                           today=datetime.now().date())


def admin_create_doctor_schedule(id):
    doctor = User.query.filter_by(id=id).first()
    form = CreateSchedule()
    if form.validate_on_submit():
        schedules = Schedule.query.filter_by(doctor_id=doctor.id)\
            .filter((Schedule.start_date.between(form.start_date.data, form.end_date.data) | (Schedule.end_date.between(form.start_date.data, form.end_date.data)) | \
                 ((Schedule.start_date <= form.start_date.data) & (Schedule.end_date >= form.end_date.data)))).all() 
        if schedules:
            flash('Schedules date Confilcted', 'warning')
            return redirect(url_for('get_and_create_doctor_schedule', id=doctor.id))
        if form.start_date.data <= form.end_date.data:
            Schedule(form.name.data, doctor.id, form.start_date.data, form.end_date.data, form.description.data)
            return redirect(url_for('get_and_create_doctor_schedule', id=doctor.id))
        flash("Please choose proper date", 'info')
        return render_template("adminPanel/doctor_schedule_list.html", doctorName=doctor.name, schedules=doctor.schedule, form=form)
    return render_template("adminPanel/doctor_schedule_list.html", doctorName=doctor.name, schedules=doctor.schedule, form=form)


def delete_doctor_schedule(id):
    schedule_delete = Schedule.query.filter_by(id=id).first()
    id = schedule_delete.doctor_id
    schedule_delete.delete_doctor_schedule()
    if request.url == base_url+"/delete/schedule/"+str(schedule_delete.id):
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
    page = request.args.get('page', 1, type=int)
    patient_list = db.session.query(User.name, User.lastname, User.phone, User.gender, Appointment.reason,
                                    Appointment.appointment_date, Appointment.state, Appointment.id)\
                    .join(Appointment, User.id == Appointment.patient_id).filter(Appointment.schedule_id == id).paginate(page=page, per_page=8)
    return render_template('appointed_patients.html', patients=patient_list)


def all_appointed_patient_list():
    page = request.args.get('page', 1, type=int)
    all_appointed_patient = db.session.query(User.name, User.lastname, User.phone, User.gender, Appointment.reason,
                                             Appointment.id, Appointment.appointment_date, Appointment.state)\
                              .join(Appointment, User.id == Appointment.patient_id).paginate(page=page, per_page=7)
    return render_template('adminPanel/appointment_list.html', patients=all_appointed_patient)


def get_user_info(id):
    user_info = User.query.filter_by(id=id).first()
    if request.method == "POST":
        user_info.update_user(request.form.get('name'), request.form.get('lastname'), request.form.get('username'),
                              request.form.get('email'), request.form.get('address'), request.form.get('phone'),
                              user_info.date_of_birth, user_info.gender, user_info.role)
        flash("The Account updated successfully!", 'info')
        return redirect(url_for("users"))
    return render_template('user_info.html', user=user_info)


def delete_an_appointment(id):
    selected_appointment = Appointment.query.filter_by(id=id).first()
    selected_appointment.delete_appointment()
    return redirect(url_for('appointed_patient_list'))


def current_user_profile():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.update_user(form.name.data, form.lastname.data, form.username.data, form.email.data,
                                 form.address.data, form.phone.data, form.date_of_birth.data, current_user.gender,
                                 current_user.role)
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


def update_user_password():
    form = ChangePassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.previous_password.data):
            new_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = new_password
            db.session.commit()
            flash('Your password changed Successfully!', 'info')
            if request.url == base_url + "/admin/change/password":
                return redirect(url_for('admin_profile'))
            return redirect(url_for('profile'))
        flash("Your old password isn't correct!", 'warning')
    if request.url == base_url + "/admin/change/password":
        return render_template("/adminPanel/admin_update_password.html", form=form)
    return render_template('/update_password.html', form=form)


def change_patient_appointment_state(id):
    desired_appointment = Appointment.query.filter_by(id=id).first()
    state = request.args.get('state')
    desired_appointment.change_appointment_state(state)
    if request.url == base_url + "/change/patient/appointment/state/" + str(id) + "?state=cancel":
        return redirect(url_for('user_appointment_list'))
    elif request.url == base_url + "/admin/change/patient/appointment/state/" \
                                 + str(id) + "?state=" + request.args.get("state"):
        return redirect(url_for('appointed_patient_list'))
    return redirect(url_for('appointed_patient', id=desired_appointment.schedule_id))

