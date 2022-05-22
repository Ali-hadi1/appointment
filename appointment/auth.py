from flask import render_template, redirect, url_for, request, flash
from appointment.forms import UserRegisteration, Login, ForgotPassword, ResetPassword
from appointment import bcrypt, db, mail
from flask_login import login_user, current_user
from appointment.Models.UserModel import User
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message

serializer = URLSafeTimedSerializer('thismustbesecret')

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
        # user = User.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.role == 2:
            doctor_info = user.doctorinfo
            if doctor_info.valid == False:
                flash('Dear Doctor your Account is not activate yet!', 'info')
                return redirect(url_for('home'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.role == 1:
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("check your username or password!", 'danger')
    return render_template("login.html", form=form)


def user_forgot_password():
    form = ForgotPassword()
    if form.validate_on_submit():
        token = serializer.dumps(form.email.data, salt='forgot-password')
        user = User.query.filter_by(email=form.email.data).first()
        msg = Message(subject="Forgot Password", sender="info@test.com", recipients=[form.email.data])
        reset_password_link = url_for('reset_password', token=token, _external=True)
        msg.html = render_template('/auth/forgot_password_mail_template.html', user=user, link=reset_password_link)
        mail.send(msg)
        flash("Reset Password link sent in your Email", 'info')
        return redirect(url_for('login'))
    return render_template('/auth/forgot_password.html', form=form)


def user_reset_password(token):
    form = ResetPassword()
    email = serializer.loads(token, salt='forgot-password', max_age=1200)
    user = User.query.filter_by(email=email).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('your password reset successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('/auth/reset_password.html', form=form)

