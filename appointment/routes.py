from flask import Flask, render_template, url_for, flash, redirect, request
from appointment import app, db, bcrypt
from functools import wraps
from appointment.models import User, DoctorInfo, Schedule, Appointment
from appointment.forms import UpdateAccount, UserRegisteration, Login, DoctorInfoForm, CreateSchedule, MakeAppointment
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import and_


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user and current_user.role == 1:
            return f(*args, **kwargs)
        flash("Ooops login or your privilage is not satisfied", "info")
        return redirect(url_for('home'))
    return wrap

def doctor_or_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user and (current_user.role == 1 or current_user.role == 2) :
            return f(*args, **kwargs)
        flash("Ooops login or your privilage is not satisfied", "info")
        return redirect(url_for('home'))
    return wrap

@app.route("/dashboard")
@admin_required
def dashboard():
    if current_user.role == 1:
        doc_request = DoctorInfo.query.filter_by(valid=False).all()
        count = len(doc_request)
        return render_template("dashboard.html", count = count)
    else:
        flash("Oops, you haven't right privilage", 'info')
        return redirect(url_for('home'))

@app.route("/")
@app.route("/home")
def home():
    doctors = db.session.query(User.id, User.name, User.lastname,User.email, DoctorInfo.degree,DoctorInfo.specialty).join(User, User.id == DoctorInfo.user_id).filter(DoctorInfo.valid==True).all()
    return render_template("home.html", doctors = doctors)


@app.route("/register", methods=['GET','POST'])
def register():
    form = UserRegisteration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, lastname=form.lastname.data, email=form.email.data, username=form.username.data,
            address = form.address.data, date_of_birth = form.date_of_birth.data, phone= form.phone.data,
            role=form.role.data ,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        stored_user = User.query.filter_by(email=form.email.data).first()
        if form.role.data == '2':
            return redirect(url_for('doctor', id = stored_user.id))
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/doctor/<int:id>", methods=('GET', 'POST'))
def doctor(id):
    form = DoctorInfoForm()
    if form.validate_on_submit():
        doc_info= DoctorInfo(user_id = id , degree=form.degree.data, specialty=form.specialty.data)
        db.session.add(doc_info)
        db.session.commit()
        flash("Your Info submited successfully wait for confimation!", 'info')
        return redirect(url_for('home'))
    return render_template('doctor_info_form.html',form=form)

@app.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.role == 2:
            doctor_info = user.doctorinfo
            if doctor_info[0].valid == False:
                flash('Dear Doctor your Account is not activate yet!', 'info')
                return redirect(url_for('home'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.role == 1:
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("check your email or password!", 'danger')
    return render_template("login.html", form=form)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile", methods=('GET', 'POST'))
@login_required
def profile():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.email.data != current_user.email:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash("This email already exist!", 'warning')
                return redirect(url_for('profile'))
        current_user.name = form.name.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.phone = form.phone.data
        current_user.date_of_birth = form.date_of_birth.data
        db.session.commit()
        flash('Your account Updated Successfully', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
        form.date_of_birth.data = current_user.date_of_birth
    return render_template('profile.html', user=current_user , form=form)

@app.route("/requests")
@admin_required
def requests():
    data = db.session.query(User.id, User.name, User.lastname,User.email, User.date_of_birth, DoctorInfo.degree,DoctorInfo.specialty, User.gender, DoctorInfo.valid).join(User, User.id == DoctorInfo.user_id).filter(DoctorInfo.valid==False).all()
    # doctors = [ i for i in data if i.valid==False]
    return render_template('request_table.html', doctors = data)


@app.route("/users")
@admin_required
def users():
    users = User.query.all()
    return render_template("/usersList.html", users=users)

@app.route("/delete/<int:id>")
@admin_required
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

@app.route("/confirm/<int:id>")
@admin_required
def confirm(id):
    doc = DoctorInfo.query.filter_by(user_id=id).first()
    doc.valid = True
    db.session.commit()
    return redirect(url_for('requests'))

@app.route("/schedule", methods=('GET', 'POST'))
@doctor_or_admin_required
def schedule():
    form = CreateSchedule()
    if form.validate_on_submit():
        create_schedule = Schedule(doctor_id = current_user.id, start_date=form.start_date.data, end_date = form.end_date.data)
        db.session.add(create_schedule)
        db.session.commit()
        return render_template('/schedule.html', form=form, schedules=current_user.schedule)
    return render_template("/schedule.html", form=form, schedules=current_user.schedule)

@app.route("/appointment", methods=('GET', 'POST'))
@admin_required
def appointment():
    return render_template("/appointment.html")

@app.route("/doctor_schedule/<int:id>", methods=('GET', 'POST'))
def viewSchedule(id):
    form = MakeAppointment()
    doctor = User.query.filter_by(id=id).first()
    return render_template("view_schedules.html", schedules=doctor.schedule, form=form)

@app.route("/patient/appointment/<int:id>", methods=('GET', 'POST'))
@login_required
def patientAppointment(id):
    patient_create_appointment = MakeAppointment()
    patient_create_appointment.schedule_id.data = id
    seleted_schedule = Schedule.query.filter_by(id=id).first()
    if patient_create_appointment.validate_on_submit():
        incoming_date_exist = db.session.query(Appointment).filter(and_(Appointment.schedule_id == id,
                                                Appointment.appointment_date == patient_create_appointment.date.data)).all()
        if incoming_date_exist:
            flash("this date booked before Please choose a different one!", "info")
            return redirect(url_for('patientAppointment', id=id))
        new_patient_appointment = Appointment(schedule_id=patient_create_appointment.schedule_id.data,
                                              patient_id = current_user.id,
                                              reason = patient_create_appointment.reason.data,
                                              appointment_date=patient_create_appointment.date.data)
        db.session.add(new_patient_appointment)
        db.session.commit()
        doctor_id = Schedule.query.filter_by(id = id).first()
        return redirect(url_for('viewSchedule', id=doctor_id.doctor_id))
    return render_template('patientAppointment.html', form = patient_create_appointment, seleted_schedule = seleted_schedule, today = datetime.now().date())

@app.route("/admin/doctors/schedules", methods=('GET', 'POST'))
@admin_required
def doctorsSchedules():
    doctors = db.session.query(User).join(Schedule, Schedule.doctor_id == User.id).group_by(User.id).all()
    return render_template("/doctors_schedules.html", doctors = doctors)

@app.route("/admin/doctors/schedules/detials/<int:id>", methods=('GET', 'POST'))
@admin_required
def doctorScheduleDetials(id):
    doctor = User.query.filter_by(id = id).first()
    create_schedule = CreateSchedule()
    return render_template("/adminPanel/doctor_schedule_list.html", schedules = doctor.schedule, form=create_schedule)

@app.route("/admin/doctors/schedules/delete/<int:id>")
@admin_required
def DeleteDoctorSchedule(id):
    schedule_delete = Schedule.query.filter_by(id=id).first()
    id = schedule_delete.doctor_id
    db.session.delete(schedule_delete)
    db.session.commit()
    return redirect(url_for('doctorScheduleDetials', id = id))

@app.route("/admin/doctors/schedules/edit/<int:id>")
@admin_required
def EditDoctorSchedule(id):
    form = CreateSchedule()
    if form.validate_on_submit():
        pass
    schedule_for_edit = Schedule.query.filter_by(id=id).first()
    form.start_date.data = schedule_for_edit.start_date
    form.end_date.data = schedule_for_edit.end_date
    return redirect(url_for('doctorScheduleDetials', id = id))
