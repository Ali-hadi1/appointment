from flask import Flask, render_template, url_for, flash, redirect, request
from appointment import app, db, bcrypt
from appointment.auth import create_account, user_login, admin_required, doctor_or_admin_required
from appointment.view import create_doctor_info, delete_user, create_schedule, view_doctor_schedule,\
                             patient_create_appointment, admin_create_doctor_schedule, delete_doctor_schedule,\
                             edit_doctor_schedule
from functools import wraps
from appointment.models import User, DoctorInfo, Schedule, Appointment
from appointment.forms import UpdateAccount, UserRegisteration, Login, DoctorInfoForm, CreateSchedule, MakeAppointment
from flask_login import login_user, current_user, logout_user, login_required

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
    return create_account()


@app.route("/doctor/<int:id>", methods=('GET', 'POST'))
def doctor(id):
    return create_doctor_info(id)


@app.route("/login", methods=('GET', 'POST'))
def login():
    return user_login()


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
    return delete_user(id)


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
    return create_schedule()


@app.route("/appointment", methods=('GET', 'POST'))
@admin_required
def appointment():
    return render_template("appointment.html")


@app.route("/doctor/schedule/<int:id>", methods=('GET', 'POST'))
def viewSchedule(id):
    return view_doctor_schedule(id)


@app.route("/patient/appointment/<int:id>", methods=('GET', 'POST'))
@login_required
def patientAppointment(id):
    return patient_create_appointment(id)


@app.route("/admin/doctors/schedules", methods=('GET', 'POST'))
@admin_required
def doctorsSchedules():
    doctors = db.session.query(User).join(Schedule, Schedule.doctor_id == User.id).group_by(User.id).all()
    return render_template("/doctors_schedules.html", doctors=doctors)


@app.route("/admin/doctors/schedules/details/<int:id>", methods=('GET', 'POST'))
@admin_required
def get_and_create_doctor_schedule(id):
    return admin_create_doctor_schedule(id)


@app.route("/admin/doctors/schedules/delete/<int:id>")
@doctor_or_admin_required
def DeleteDoctorSchedule(id):
    return delete_doctor_schedule(id)


@app.route("/admin/doctors/schedules/edit/<int:id>", methods=['GET', 'POST'])
@admin_required
def admin_edit_doctor_schedule(id):
    return edit_doctor_schedule(id)


@app.route("/doctors/schedules/edit/<int:id>", methods=['GET', 'POST'])
@doctor_or_admin_required
def doctor_edit_schedule(id):
    return edit_doctor_schedule(id)
