from flask import Flask, render_template, request, redirect
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

@app.route("/")
def hello():
    return render_template("index.html")

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
            return redirect("")

    #Need different redirect pages
    return redirect("")

@app.route('/find', methods=['GET', 'POST'])
def find():
    form = PathFinderForm()
    form.study.choices = CategoryModel.get_distinct_study()

    study_name = form.study.choices[0][1]

    form.category.choices = CategoryModel.get_distinct_category(study_name)

    category = form.category.choices[0][1]

    form.value.choices = CategoryModel.get_distinct_value(category)


    if request.method == "POST":
        study_name, category, value = CategoryModel.get_all_with_id(request.form['value'])
        path_list = CategoryModel.get_path_list(study_name, category, value)
        return render_template("display_path.html", result=path_list)

    return render_template('display.html', form=form)

@app.route('/value/<category_id>')
def value(category_id):
    return CategoryModel.get_value_by_category_id(category_id)

@app.route('/category/<study_id>')
def category(study_id):
    return CategoryModel.get_category_by_study_id(study_id)


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
