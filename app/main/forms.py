from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired, Length


class ApplyForm(FlaskForm):
    name = TextField('Your Name', validators=[DataRequired(), Length(min=6, max=25)])
    location = TextField('Location', validators=[DataRequired(), Length(min=6, max=40)])
    linkedin_handle = TextField('Linkedin', validators=[DataRequired(), Length(min=6, max=40)])
    submit = SubmitField('Submit')
