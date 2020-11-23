from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    term = StringField('Search Term')
    submit = SubmitField('Search')