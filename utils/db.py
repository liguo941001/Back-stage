#!/usr/bin/env python
#coding: utf-8

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa


Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    name = sa.Column(sa.String)
    gender = sa.Column(sa.Boolean) # 性别, True: Male, False: Female
    born = sa.Column(sa.DateTime)  # 生日
    tags = sa.Column(sa.String)    # 测试用的Tag


def init_db():    
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session
    
engine, session = init_db()


def fill_users():
    for i in range(1, 201):
        user = User()
        user.age = i
        user.name = 'NAME-{0}'.format(i)
        user.gender = True if i%2 == 1 else False
        user.born = datetime.now() - timedelta(seconds=i)
        session.add(user)
        
    session.commit()


def test_query_users():
    users = session.query(User).all()
    for u in users:
        print u.age, u.name, u.gender, u.born, u.tags


fill_users()
test_query_users()
