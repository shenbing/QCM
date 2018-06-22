# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from app.home import home
from flask import render_template,abort
from flask.views import MethodView,View
from flask_login import current_user
from flask import redirect,url_for
from flask_login import login_required

class IndexView(MethodView):
    @login_required
    def get(self):
        if current_user.is_authenticated:
            return render_template("home/index.html")
        else:
            return redirect(url_for("auth.login"))