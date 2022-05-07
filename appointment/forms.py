from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField, SelectField, TextAreaField, HiddenField
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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("this Username already exist!")


class UpdateAccount(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=8)])
    username = StringField('username', validators=[DataRequired(), Length(min=4)])
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

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("this Username already exist!")

class Login(FlaskForm):
    # email = StringField('email', validators=[DataRequired(), Email()])
    username = StringField('username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DoctorInfoForm(FlaskForm):
    degree = SelectField('degree', validators=[DataRequired()],
             choices=[("something1","degree 1"),("something2","Degree 2"),("something3","Degree 3")] )
    specialty = StringField('speciality', validators=[DataRequired(), Length(min=4 , max=200)])
    submit = SubmitField('submit')


class CreateSchedule(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=4, max=20)])
    start_date = DateField('start_date', validators=[DataRequired()])
    end_date = DateField('end_date', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    submit = SubmitField('submit')


class MakeAppointment(FlaskForm):
    schedule_id= HiddenField('schedule_id')
    reason = TextAreaField('reason', validators=[DataRequired()])
    date = DateField('end_date', validators=[DataRequired()])
    submit = SubmitField('submit')


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
