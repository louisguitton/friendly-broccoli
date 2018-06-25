from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from config import global_data
# Set your classes here.



class ApplyForm(FlaskForm):
    name = TextField(
        'Your Name', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    location = TextField(
        'Location', validators=[DataRequired(), Length(min=6, max=40)]
    )
    linkedin = TextField(
        'Linkedin', validators=[DataRequired(), Length(min=6, max=40)]
    )
    submit = SubmitField('Submit')
    

class RegisterForm(FlaskForm):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(FlaskForm):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(FlaskForm):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
