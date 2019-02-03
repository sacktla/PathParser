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
    form.category.choices = CategoryModel.get_distinct_category()

    if request.method == "POST":
        return "" #This is where i can query the paths and present them

    return render_template('display.html', form=form)

@app.route('/value/<category_id>')
def value(category_id):
    return CategoryModel.get_value_by_category_id(category_id)


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
