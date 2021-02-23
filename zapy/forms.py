from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('Jak masz na imie?', validators=[DataRequired()])
    submit = SubmitField('Submit')
