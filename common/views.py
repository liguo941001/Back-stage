#coding: utf-8

from flask import Blueprint

bp = Blueprint('common', __name__)


@bp.route('/login')
def login():
    return 'login'


@bp.route('/logout')
def logout():
    return 'logout'
