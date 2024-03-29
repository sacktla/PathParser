from db import db
from flask import jsonify

class PathModel(db.Model):
    __tablename__ = "path"

    id         = db.Column(db.Integer, primary_key=True)
    path       = db.Column(db.String(80), unique=True, nullable=False)
    categories = db.relationship("CategoryModel", lazy="dynamic")

    def __init__(self, path):
        self.path = path

    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()

        return self.id

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_path_name(cls, path_id):
        return cls.query.filter_by(id=path_id).first().path


class CategoryModel(db.Model):
    __tablename__ = "category"

    id         = db.Column(db.Integer, primary_key=True)
    study_name = db.Column(db.String(80), nullable=False)
    category   = db.Column(db.String(80), nullable=False)
    value      = db.Column(db.String(80), nullable=False)
    data_type  = db.Column(db.String(80))
    path_id    = db.Column(db.Integer, db.ForeignKey('path.id'), nullable=False)
    path       = db.relationship("PathModel")


    def __init__(self, study_name, category, value, data_type, path_id):
        self.study_name = study_name
        self.category   = category
        self.value      = value
        self.path_id    = path_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_distinct_study(cls):
        distinct = []
        for item in cls.query.group_by(CategoryModel.study_name).all():
            distinct.append((item.id, item.study_name))

        return distinct

    @classmethod
    def get_distinct_category(cls, study_name):
        distinct = []
        for item in cls.query.filter_by(study_name=study_name).group_by(CategoryModel.category).all():
            distinct.append((item.id, item.category))

        return distinct

    @classmethod
    def get_category_by_study_id(cls, study_id):
        study_name = CategoryModel.query.filter_by(id=study_id).first().study_name
        categories = []

        for item in cls.query.filter_by(study_name=study_name).group_by(CategoryModel.category).all():
            categoryDict = {}
            categoryDict['id'] = item.id
            categoryDict['category'] = item.category

            categories.append(categoryDict)

        return jsonify({'categories': categories})

    @classmethod
    def get_all_with_id(cls, search_params, search_params_bool):
        result = cls.query
        if search_params_bool[0]:
            study_name = cls.query.filter_by(id=search_params[0]).first().study_name
            result = result.filter_by(study_name=study_name)

        if search_params_bool[1]:
            category = cls.query.filter_by(id=search_params[1]).first().category
            result   = result.filter_by(category=category).filter_by(value=search_params[2])

        paths = []
        for item in result.group_by(CategoryModel.path_id):
            paths.append(PathModel.get_path_name(item.path_id))
        return paths
