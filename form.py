from model import CategoryModel, PathModel
from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, SelectMultipleField

class PathFinderForm(FlaskForm):
    study = SelectField('study', choices=[])
    study_checkbox = BooleanField('study_bool')
    category = SelectField('category', choices=[])
    category_checkbox = BooleanField('category_bool')
    value = SelectField('value', choices=[])
    value_checkbox = BooleanField('value_bool')
