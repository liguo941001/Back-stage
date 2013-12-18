#coding: utf-8

import json
from flask import Blueprint, request, redirect, url_for, render_template
from .models import User
from .jsontable import pre_process, get_data

bp = Blueprint('common', __name__)


TABLES = {
    'users': {
        'model': User,
        'columns': [
            {'key': 'age', 'head': u'年龄'},
            {'key': 'name', 'head': u'名字',
             'type': 'link',
             'link': lambda record: url_for('common.users_edit', oid=record.id)},
            {'key': 'gender', 'head': u'性别', 'sortable': False},
            {'key': 'birthday', 'head': u'生日'},
            # {'key': 'tags', 'head': u'标签'}
        ],
        'actions': {
            'edit': {'endpoint': 'common.users_edit'},
            'del': {'endpoint': 'common.users_del'},
        }
    }
}

pre_process(TABLES)

@bp.route('/')
def index():
    return redirect(url_for('common.users'))

    
@bp.route('/users')
def users():
    return render_template('users.html')


@bp.route('/users.json')
def users_json():
    data = get_data(request, TABLES['users'])
    data['title'] = u'用户列表'
    return json.dumps(data)
    

@bp.route('/users/edit')
def users_edit():
    oid = request.values.get('oid', None)
    return 'oid:' +  oid
    

@bp.route('/users/del', methods=['POST'])
def users_del():
    oids = request.values.get('oids', None)
    return 'oids:' +  oids
    
