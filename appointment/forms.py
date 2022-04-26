from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from appointment.models import User

class UserRegisteration(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2 , max=8)])
    username = StringField('username', validators=[DataRequired(), Length(min=4)])
    email = StringField('email',validators=[DataRequired(), Email()])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=4 , max=8)])
    address = StringField('address', validators=[DataRequired(), Length(max=200)])
    date_of_birth = DateField('date_of_birth', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), Length(min=10, max=14)])
    role = SelectField('Register As', choices=[(2, 'Doctor'), (3, 'Patient')])
    gender = RadioField("gender", choices=['male','female'])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("this email already exist!")

class UpdateAccount(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=8)])
    email = StringField('email', validators=[DataRequired(), Email()])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=4, max=8)])
    address = StringField('address', validators=[DataRequired(), Length(max=200)])
    date_of_birth = DateField('date_of_birth', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), Length(min=10, max=14)])
    submit = SubmitField('update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("this email already exist!")

class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DoctorInfoForm(FlaskForm):
    degree = SelectField('degree', validators=[DataRequired()],
             choices=[("something1","degree 1"),("something2","Degree 2"),("something3","Degree 3")] )
    specialty = StringField('speciality', validators=[DataRequired(), Length(min=4 , max=200)])
    submit = SubmitField('submit')

class CreateSchedule(FlaskForm):
    start_date = DateField('start_date', validators=[DataRequired()])
    end_date = DateField('end_date', validators=[DataRequired()])
    submit = SubmitField('submit')