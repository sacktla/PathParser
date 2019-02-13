from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from PathParser import PathParser
from model import CategoryModel, PathModel
from form import PathFinderForm
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = 'secret'

@app.before_first_request
def create_tables():
    db.create_all()

"""
Display homepage with the ability to add paths or redirect you to
the page to search params.
"""
@app.route("/")
def index():
    return render_template("index.html")

"""
Parses path passed for study passed. If successful it will alert the user
that the path was successfully stored as a flash alert and refresh the
homepage. If the path is not successfully stored, a flash alert will let
the user know.
"""
@app.route("/parse", methods=["POST"])
def parse():
    path       = request.form['path']
    study      = request.form['study']
    parser     = PathParser(path, study)
    data_load  = parser.path_dict
    path_model = PathModel(path)

    if path_model:
        try:
            parent_id = path_model.save_to_db()

            for key in data_load:

                value     = data_load[key]['value']
                data_type = data_load[key]['data_type']
                category  = CategoryModel(study, key, value, data_type, parent_id)

                category.save_to_db()

            return render_template('display.html', result={'data_load': data_load, \
                                                            'path': path,\
                                                            'study': study})
        except:
            #Alert that the path already existed
            return redirect("")
    #Alert that the database connection failed
    return redirect("")

"""
Directs you to the page where you can search a file path or to the list of
paths if you clicked search. It allows you to search based on study, category
and/or values. If
"""
@app.route('/find', methods=['GET', 'POST'])
def find():

    if request.method == "POST":
        form               = PathFinderForm()
        study_checked      = form.study_checkbox.data
        study              = form.study.data
        category           = form.category.data
        value_checked      = form.value_checkbox.data
        value              = form.value.data
        search_params_bool = [study_checked, value_checked]
        search_params      = [study, category, value]
        path_list          = CategoryModel.get_all_with_id(search_params, search_params_bool)

        return render_template("display_path.html", result=path_list)

    form                  = PathFinderForm()
    form.study.choices    = CategoryModel.get_distinct_study()
    study_name            = form.study.choices[0][1]
    form.category.choices = CategoryModel.get_distinct_category(study_name)

    return render_template('display.html', form=form)

"""
Returns all the categories found per study id
"""
@app.route('/category/<study_id>')
def category(study_id):
    return CategoryModel.get_category_by_study_id(study_id)


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
