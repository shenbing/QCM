# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from . import home
from flask import render_template,abort
from flask.views import MethodView,View
from .form import LoginFrom

class LoginView(MethodView):
    def get(self):
        form=LoginFrom()
        return render_template('home/index.html', form=form)

    def post(self):
        pass