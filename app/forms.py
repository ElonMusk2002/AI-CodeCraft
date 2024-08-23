# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProfileForm(FlaskForm):
    skill_level = IntegerField(
        "Skill Level", validators=[DataRequired(), NumberRange(min=1, max=10)]
    )
    preferred_languages = StringField(
        "Preferred Programming Languages", validators=[DataRequired()]
    )
    preferred_topics = StringField("Preferred Topics", validators=[DataRequired()])
    submit = SubmitField("Update Profile")
