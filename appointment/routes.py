from flask import Flask, render_template, url_for, flash, redirect
from appointment import app, db, bcrypt
from appointment.models import Patient
from appointment.forms import PatientRegisterationForm, DoctorRegisterationForm

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=['GET','POST'])
def register():
    form = PatientRegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        patient = Patient(name=form.name.data, lastname=form.lastname.data, email=form.email.data,
            address = form.address.data, date_of_birth = form.date_of_birth.data, phone= form.phone.data
            ,password=hashed_password)
        db.session.add(patient)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

