from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from models import User
from datetime import date
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one or login.')

class ApplicationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(), 
        Length(min=3, max=100, message="Name must be between 3 and 100 characters")
    ])
    
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    
    mobile_number = StringField('Mobile Number', validators=[
        DataRequired(),
        Regexp(r'^\d{10}$', message="Mobile number must be 10 digits")
    ])
    
    aadhar_number = StringField('Aadhar Card Number', validators=[
        DataRequired(),
        Regexp(r'^\d{12}$', message="Aadhar number must be 12 digits")
    ])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    course = SelectField('Course', validators=[DataRequired()], choices=[])
    
    photo = FileField('Upload Photo (JPG/JPEG/PNG, max 10MB)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG, JPEG or PNG images are allowed!')
    ])
    
    signature = FileField('Upload Signature (JPG/JPEG/PNG, max 10MB)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG, JPEG or PNG images are allowed!')
    ])
    
    submit = SubmitField('Preview Application')
    
    def validate_date_of_birth(self, date_of_birth):
        today = date.today()
        age = today.year - date_of_birth.data.year - ((today.month, today.day) < (date_of_birth.data.month, date_of_birth.data.day))
        if age < 16:
            raise ValidationError('You must be at least 16 years old to apply.')
        if age > 60:
            raise ValidationError('Please verify your date of birth.')

class PreviewForm(FlaskForm):
    confirm_submit = SubmitField('Submit Application')
    edit = SubmitField('Edit Application')
