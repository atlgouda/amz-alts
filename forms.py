from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class SearchForm(FlaskForm):
    term = StringField('Search Term', [validators.required()])
    submit = SubmitField('Search')