from flask import Flask, render_template, url_for, flash, redirect, request
from appointment import app, db, bcrypt
from appointment.models import User
from appointment.forms import UserRegisteration, Login, DoctorRegisterationForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == 1:
        return render_template("index.html")
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
        patient = User(name=form.name.data, lastname=form.lastname.data, email=form.email.data,
            address = form.address.data, date_of_birth = form.date_of_birth.data, phone= form.phone.data
            ,password=hashed_password)
        db.session.add(patient)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", form=form)


@app.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("check your email or passowrd!", 'danger')
    return render_template("login.html", form=form)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', user=current_user)
