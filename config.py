# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'welcome to codyy'
    WTF_CSRF_ENABLED = False
    COVERAGE = False
    MAIL_SERVER = 'mail.codyy.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'shenbing@codyy.com'
    MAIL_PASSWORD = 'aA111111'
    FLASKY_MAIL_SUBJECT_PREFIX = '[QCM]'
    FLASKY_MAIL_SENDER = 'QCM Admin <shenbing@codyy.com>'
    FLASKY_ADMIN = os.environ.get('QCM_ADMIN') or 'shenbing@codyy.com'
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG = True
    PER_PAGE = 10
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:aA111111@localhost:3306/test?charset=utf8'
    REMEMBER_COOKIE_DURATION = 1800
    ZENTAO_LOGINURL = "http://10.1.210.51:80/zentao/user-login.html"
    ZENTAO_USERNAME = 'shenbing'
    ZENTAO_PASSWORD = 'aA!111111'

    @staticmethod
    def init_app(app):
        pass
