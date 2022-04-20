from flask import Flask, render_template, url_for
from appointment import app
from appointment.forms import PatientRegisterationForm

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register")
def register():
    form = PatientRegisterationForm()
    return render_template("register.html", form=form)