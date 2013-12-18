#coding: utf-8

SECRET_KEY = 'ijk_IJK_0123'

SQLALCHEMY_DATABASE_URI = 'sqlite:///example.db'

try:
    from etc.settings import *
except:
    pass
