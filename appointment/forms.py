from random import choices
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class PatientRegisterationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2 , max=8)])
    email = StringField('email',validators=[DataRequired(), Email()])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=4 , max=8)])
    address = StringField('address', validators=[DataRequired(), Length(max=200)])
    date_of_birth = DateField('date_of_birth', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), Length(min=10, max=14)])
    status = RadioField('status', choices=['single', 'married'])
    gender = RadioField("gender", choices=['male','female'])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

class DoctorRegisterationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2 , max=8)])
    email = StringField('email',validators=[DataRequired(), Email()])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=4 , max=8)])
    address = StringField('address', validators=[DataRequired(), Length(max=200)])
    date_of_birth = DateField('date_of_birth', validators=[DataRequired()])
    dgree = SelectField('degree', validators=[DataRequired()],
             choices=[(1,"1 Degree"),(2,"2 Degree"),(3,"3 Degree")] )
    speciality = StringField('speciality', validators=[DataRequired(), Length(min=4 , max=200)])
    phone = StringField('phone', validators=[DataRequired(), Length(min=10, max=14)])
    status = RadioField('status', choices=['single', 'married'])
    gender = RadioField("gender", choices=['male','female'])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')