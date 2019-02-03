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
    def find_by_name(cls, path):
        return cls.query.filter_by(path=path).first()


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
    def get_distinct_category(cls):
        distinct = []
        for item in cls.query.group_by(CategoryModel.category).all():
            distinct.append((item.id, item.category))

        return distinct

    @classmethod
    def get_value_by_category_id(cls, category_id):
        category = CategoryModel.query.filter_by(id=category_id).first().category
        values = []
        
        for item in cls.query.filter_by(category=category).group_by(CategoryModel.value).all():
            valueDict          = {}
            valueDict['id']    = item.id
            valueDict['value'] = item.value

            values.append(valueDict)

        return jsonify({'values': values})
