from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    product = StringField('Sprawdź zapasy:', validators=[DataRequired()])
    submit = SubmitField('Szukaj')
