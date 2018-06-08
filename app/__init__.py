# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask import Flask,url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask import render_template
from .home import home

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    bootstrap = Bootstrap(app)
    loginManager = LoginManager(app)
    loginManager.login_view = "home.index"
    loginManager.session_protection = "strong"
    loginManager.login_message = "请登录QCM平台！"
    db = SQLAlchemy(app)
    moment = Moment(app)
    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html')

    #注册蓝图
    app.register_blueprint(home)

    return app
