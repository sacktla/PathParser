from model import CategoryModel, PathModel
from flask_wtf import FlaskForm
from wtforms import SelectField

class PathFinderForm(FlaskForm):
    study = SelectField('study', choices=[])
    category = SelectField('category', choices=[])
    value = SelectField('value', choices=[])
