from flask import render_template, redirect, url_for, request, flash
from appointment.forms import UserRegisteration, Login
from appointment import bcrypt
from flask_login import login_user, current_user
from appointment.models import User
from functools import wraps


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user and current_user.role == 1:
            return f(*args, **kwargs)
        flash("Ooops login or your privilege is not satisfied", "info")
        return redirect(url_for('home'))
    return wrap


def doctor_or_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user and (current_user.role == 1 or current_user.role == 2) :
            return f(*args, **kwargs)
        flash("Ooops login or your privilege is not satisfied", "info")
        return redirect(url_for('home'))
    return wrap


def create_account():
    form = UserRegisteration()
    if form.validate_on_submit():
        gender = True if form.gender.data == 'male' else False
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.name.data, form.lastname.data, form.username.data, form.email.data, form.address.data,
                    form.phone.data, form.date_of_birth.data, form.role.data, gender, hashed_password)
        if user.role == 2:
            return redirect(url_for('doctor', id=user.id))
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.role == 2:
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

