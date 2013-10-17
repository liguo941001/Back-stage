#!/usr/bin/env python
#coding: utf-8

from flask import Flask
from common.views import bp as bp_common

def create_app():

    tApp = Flask(__name__)
    tApp.config.from_pyfile('settings.py')

    blueprints = [bp_common]
    for bp in blueprints:
        tApp.register_blueprint(bp)
        
    register_jinja(tApp)
    
    ############################################################
    # Request management
    @tApp.before_request
    def before_request():
        pass

    # Error Handler
    @tApp.errorhandler(404)
    def error_404(e):
        return 'Not Found! There is nothing here......', 404

        
    @tApp.route('/')
    def index():
        return 'index'

    return tApp


def register_jinja(tApp):
    # Template Filter
    @tApp.template_filter('nullempty')
    def ifnull(value, default=""):
        return default if value is None else value

    # Template function
    @tApp.context_processor
    def context_processor():
        def demo_func():
            return 'demo processor'
            
        return { 'demo_func': demo_func }

        
app = create_app()

if __name__ == '__main__':
    import sys
    try:
        port = int(sys.argv[1])
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception, e:
        print e
