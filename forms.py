from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo)


# Functions for preventing duplicate registrations
def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Username is taken')


def email_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Email is already used')


# Form Schemata
# Login Form on login.html
class Login(FlaskForm):
    id = StringField("Username: ", validators=[DataRequired()])
    password = StringField("Password: ", validators=[DataRequired()])


# Registration Form on registration.html for creating users
class Register(FlaskForm):
    first_name = StringField("First Name: ", validators=[
        DataRequired(),
        Regexp(
            r'^[a-zA-Z\s-]+$',
            message="Names can only contain letter, spaces, and a dash"
        ),
        name_exists
    ])
    last_name = StringField("Last Name: ", validators=[
        DataRequired(),
        Regexp(
            r'^[a-zA-Z\s-]+$',
            message="Names can only contain letter, spaces, and a dash"
        ),
        name_exists
    ])
    username = StringField('Username', validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username must be 1 word, letters, numbers, and "
                         "underscores only")
            ),
            name_exists
    ])
    email = StringField('Email', validators=[
            DataRequired(),
            Email(),
            email_exists
    ])
    password = PasswordField('Password: ', validators=[
            DataRequired(),
            Length(min=4),
            EqualTo('password2',"Passwords must match")
    ])
    password2 = PasswordField('Confirm Password: ', validators=[
            DataRequired(),
    ])
