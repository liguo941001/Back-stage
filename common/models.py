# coding: utf-8

from common.gvars import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    name = db.Column(db.String)
    gender = db.Column(db.Boolean)  # 性别, True: Male, False: Female
    birthday = db.Column(db.DateTime)  # 生日
    tags = db.Column(db.String)  # 测试用的Tag
