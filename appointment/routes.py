from flask import render_template, url_for, redirect, request
from appointment import app, db
from appointment.auth import create_account, user_login, user_forgot_password, user_reset_password
from appointment.view import create_doctor_info, delete_user, create_schedule, view_doctor_schedule,\
                             patient_create_appointment, admin_create_doctor_schedule, delete_doctor_schedule,\
                             edit_doctor_schedule, appointed_patient_on_a_schedule, all_appointed_patient_list,\
                             get_user_info, delete_an_appointment, current_user_profile, get_users_with_pagenation,\
                             update_user_password, change_patient_appointment_state, confirm_doctor_request
                                 
from appointment.privilege import admin_required, doctor_required
from appointment.queries import get_all_confirmed_doctors, get_all_patients, get_all_requested_doctors,\
                                get_doctor_schedule, get_user_appointment, get_all_doctors
from appointment.Models.DoctorInfoModel import DoctorInfo
from flask_login import logout_user, login_required


@app.route("/dashboard")
@login_required
@admin_required
def dashboard():
    doc_request = DoctorInfo.query.filter_by(valid=False).all()
    count = len(doc_request)
    return render_template("dashboard.html", count=count, count_patients=len(get_all_patients()),
        count_doctors=len(get_all_confirmed_doctors())
    )


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", doctors=get_all_confirmed_doctors())


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
    return current_user_profile()


@app.route("/requests")
@login_required
@admin_required
def requests():
    return render_template('request_table.html', doctors=get_all_requested_doctors())


@app.route("/admin/users/list")
@login_required
@admin_required
def users():
    return get_users_with_pagenation()


@app.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):
    return delete_user(id)


@app.route("/confirm/<int:id>")
@login_required
@admin_required
def confirm(id):
    confirm_doctor_request(id)
    return redirect(url_for('requests'))


@app.route("/schedule", methods=('GET', 'POST'))
@login_required
@doctor_required
def schedule():
    return create_schedule()


@app.route("/appointment", methods=('GET', 'POST'))
@login_required
@admin_required
def appointment():
    return render_template("appointment.html")


@app.route("/list/<int:id>", methods=('GET', 'POST'))
def viewSchedule(id):
    return view_doctor_schedule(id)


@app.route("/patient/appointment/<int:id>", methods=('GET', 'POST'))
@login_required
def patientAppointment(id):
    return patient_create_appointment(id)


@app.route("/admin/doctors/schedules", methods=('GET', 'POST'))
@login_required
@admin_required
def doctorsSchedules():
    return render_template("/doctors_schedules.html", doctors=get_all_doctors())


@app.route("/admin/doctors/schedules/details/<int:id>", methods=('GET', 'POST'))
@login_required
@admin_required
def get_and_create_doctor_schedule(id):
    return admin_create_doctor_schedule(id)


@app.route("/admin/doctors/schedules/delete/<int:id>")
@login_required
@admin_required
def DeleteDoctorSchedule(id):
    return delete_doctor_schedule(id)


@app.route("/delete/schedule/<int:id>")
@login_required
@doctor_required
def delete_schedule(id):
    return delete_doctor_schedule(id)


@app.route("/admin/doctors/schedules/edit/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_doctor_schedule(id):
    return edit_doctor_schedule(id)


@app.route("/doctors/schedules/edit/<int:id>", methods=['GET', 'POST'])
@login_required
@doctor_required
def doctor_edit_schedule(id):
    return edit_doctor_schedule(id)


@app.route("/appointed/patient/<int:id>", methods=['GET'])
@login_required
@doctor_required
def appointed_patient(id):
    return appointed_patient_on_a_schedule(id)


@app.route("/admin/appointed/patient/list", methods=['GET'])
@login_required
@admin_required
def appointed_patient_list():
    return all_appointed_patient_list()


@app.route("/admin/user/info/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def user_info(id):
    return get_user_info(id)


@app.route("/admin/delete/appointmet/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def delete_appointment(id):
    return delete_an_appointment(id)


@app.route("/admin/profile", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_profile():
    return current_user_profile()


@app.route("/change/password", methods=['GET', 'POST'])
@login_required
def update_password():
    return update_user_password()


@app.route("/admin/change/password", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_update_password():
    return update_user_password()


@app.route('/doctor/schedule/list/<int:id>')
@login_required
@doctor_required
def doctor_schedule(id):
    return render_template("/doctor_schedules.html", schedules=get_doctor_schedule(id)) 


@app.route('/user/appointment/list')
@login_required
def user_appointment_list():
    return render_template("/patient_appointment_list.html", appointments=get_user_appointment())


@app.route('/user/appointment/list/<int:id>')
@login_required
def cancel_appointed_date(id):
    return render_template("/patient_appointment_list.html", appointments=get_user_appointment(id))


@app.route('/doctor/change/patient/appointment/state/<int:id>')
@login_required
@doctor_required
def doctor_change_appointment_state(id):
    return change_patient_appointment_state(id)


@app.route('/admin/change/patient/appointment/state/<int:id>')
@login_required
@admin_required
def admin_change_appointment_state(id):
    return change_patient_appointment_state(id)


@app.route('/change/patient/appointment/state/<int:id>')
@login_required
def patient_change_appointment_state(id):
    return change_patient_appointment_state(id)


@app.route('/forgot/password', methods=['GET', 'POST'])
def forgot_password():
    return user_forgot_password()


@app.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    return user_reset_password(token)

