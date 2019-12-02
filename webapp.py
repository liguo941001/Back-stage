#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from common.models import User
from common.views import bp as bp_common
from common.gvars import db


def create_app():
    tApp = Flask(__name__)
    tApp.config.from_pyfile('settings.py')

    blueprints = [bp_common]
    for bp in blueprints:
        tApp.register_blueprint(bp)

    db.init_app(tApp)
    db.app = tApp
    # init_db(tApp)

    return tApp


def init_db(tApp):
    from datetime import datetime, timedelta

    db.create_all()
    for i in range(1, 201):
        user = User()
        user.age = i
        user.name = 'NAME-{0}'.format(i)
        user.gender = True if i % 2 == 1 else False
        user.birthday = datetime.now() - timedelta(seconds=i)
        db.session.add(user)

    db.session.commit()
    print('Database Init completed!')
    # for u in User.query.all(): print u.age, u.name, u.gender, u.birthday, u.tags


app = create_app()

if __name__ == '__main__':
    import sys

    try:
        port = int(sys.argv[1])
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(e)
