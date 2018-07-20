# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from app.bug import bug
from app import Config
from flask import render_template,abort
from flask.views import MethodView,View
from flask_login import current_user
from flask import redirect,url_for
from flask_login import login_required
from app.common.ZentaoParser import ZentaoParser
from app.common import threads_function

class BugsPerDayView(MethodView):
    @login_required
    def get(self):
        if current_user.is_authenticated:
            return render_template("bug/bugsPerDay.html", form = threads_function.newlybugdic)
        else:
            return redirect(url_for("auth.login"))

class BugsStatusView(MethodView):
    @login_required
    def get(self):
        if current_user.is_authenticated:
            return render_template("bug/bugsStatus.html", form=threads_function.bugstatusdic)
        else:
            return redirect(url_for("auth.login"))