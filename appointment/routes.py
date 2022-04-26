from flask import Flask, render_template, url_for, flash, redirect, request
from appointment import app, db, bcrypt
from appointment.models import User, DoctorInfo, Schedule
from appointment.forms import UpdateAccount, UserRegisteration, Login, DoctorInfoForm, CreateSchedule
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/dashboard")
@login_required
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
    return render_template("home.html")


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
def requests():
    data = db.session.query(User.id, User.name, User.lastname,User.email, User.date_of_birth, DoctorInfo.degree,DoctorInfo.specialty, User.gender, DoctorInfo.valid).join(User, User.id == DoctorInfo.user_id).filter(DoctorInfo.valid==False).all()
    # doctors = [ i for i in data if i.valid==False]
    return render_template('request_table.html', doctors = data)


@app.route("/users")
def users():
    users = User.query.all()
    return render_template("/usersList.html", users=users)

@app.route("/delete/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

@app.route("/confirm/<int:id>")
def confirm(id):
    doc = DoctorInfo.query.filter_by(id=id).first()
    doc.valid = True
    db.session.commit()
    return redirect(url_for('requests'))

@app.route("/schedule", methods=('GET', 'POST'))
def schedule():
    schedules = Schedule.query.all()
    form = CreateSchedule()
    if form.validate_on_submit():
        sche = Schedule(doctor_id = current_user.id, start_date=form.start_date.data, end_date = form.end_date.data)
        db.session.add(sche)
        db.session.commit()
        return render_template('/schedule.html', form=form, schedules=schedules)
    return render_template("/schedule.html", form=form, schedules=schedules)

@app.route("/appointment", methods=('GET', 'POST'))
def appointment():
    return render_template("/appointment.html")
