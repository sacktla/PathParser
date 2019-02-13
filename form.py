from model import CategoryModel, PathModel
from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, StringField

class PathFinderForm(FlaskForm):
    study             = SelectField('study', choices=[])
    study_checkbox    = BooleanField('study_bool')
    category          = SelectField('category', choices=[])
    value             = StringField('value')
    value_checkbox    = BooleanField('value_bool')
