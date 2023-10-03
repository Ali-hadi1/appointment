from logging import PlaceHolder
from flask import flash
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from appointment.Models.UserModel import User
from datetime import datetime
from re import search



class UserRegisteration(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2 , max=20),
                        Regexp('^\w+$', message="Your name must contain alphanumric or underscore")])
    username = StringField('Username', validators=[DataRequired(), Length(min=4),
                        Regexp('^\w+$', message="Your username must contain alphanumric or underscore")])
    email = StringField('Email',validators=[DataRequired(), Email()])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=4 , max=20),
                        Regexp('^\w+$', message="Your lastname must contain alphanumric or underscore")])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    date_of_birth = DateField('Date Of Birth', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=14)])
    role = SelectField('Register As', choices=[(2, 'Doctor'), (3, 'Patient')])
    gender = RadioField("Gender", choices=['male','female'])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("this email already exist!")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("this Username already exist!")
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError("this Phone number already exist!")


class UpdateAccount(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=8),
                    Regexp('^\w+$', message="Your name must contain alphanumric or underscore")])
    username = StringField('Username', validators=[DataRequired(), Length(min=4),
                    Regexp('^\w+$', message="Your username must contain alphanumric or underscore")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=4, max=8),
                    Regexp('^\w+$', message="Your lastname must contain alphanumric or underscore")])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    date_of_birth = DateField('Date Of Birth', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=14)])
    submit = SubmitField('update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("this email already exist!")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("this Username already exist!")

class Login(FlaskForm):
    # email = StringField('email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4),
                    Regexp('^\w+$', message="Your username must contain alphanumric or underscore")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DoctorInfoForm(FlaskForm):
    degree = SelectField('Degree', validators=[DataRequired()],
             choices=[("something1","degree 1"),("something2","Degree 2"),("something3","Degree 3")] )
    specialty = StringField('Speciality', validators=[DataRequired(), Length(min=4 , max=200)])
    submit = SubmitField('submit')

    def validate_specialty(self, specialty):
        if not search('^[\w\s]+$', specialty.data):
            raise ValidationError("Enter valid specialty")


class CreateSchedule(FlaskForm):
    name = StringField('Title', validators=[DataRequired(), Length(min=4, max=20)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('submit')

    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError("Please choose a proper date!")

    def validate_description(self, description):
        if not search('^[\w\s]+', description.data):
            flash("Please enter valid description", 'danger')
            raise ValidationError('Please enter valid description!')
    
    def validate_start_date(self, start_date):
        if start_date.data < datetime.now().date():
            raise ValidationError('The Start Date should be higher or equal to the today date!')


class MakeAppointment(FlaskForm):
    schedule_id= HiddenField('schedule_id')
    reason = TextAreaField('reason', validators=[DataRequired()])
    date = DateField('Select Appointment Date', validators=[DataRequired()])
    submit = SubmitField('submit')

    def validate_date(self, date):
        if date.data < datetime.now().date():
            raise ValidationError("This date is expired!", 'warning')

    def validate_reason(self, reason):
        if not search('^[\w\s]+', reason.data):
            raise ValidationError('Please enter valid reason!')


class EditUserInfo(FlaskForm):
    user_id = HiddenField('user_id')
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=8)])
    username = StringField('username', validators=[DataRequired(), Length(min=4)])
    email = StringField('email', validators=[DataRequired(), Email()])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=4, max=8)])
    address = StringField('address', validators=[DataRequired(), Length(max=200)])
    date_of_birth = DateField('date_of_birth', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), Length(min=10, max=14)])
    role = SelectField('Register As', choices=[(2, 'Doctor'), (3, 'Patient'), (1, 'admin')])
    gender = RadioField("gender", choices=['male', 'female'])
    submit = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("this email already exist!")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("this Username already exist!")


class ChangePassword(FlaskForm):
    previous_password = PasswordField('previous password', validators=[DataRequired()])
    new_password = PasswordField('new password', validators=[DataRequired()])
    submit = SubmitField('update password')


class ForgotPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
             raise ValidationError("this email is not exist")


class ResetPassword(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')
