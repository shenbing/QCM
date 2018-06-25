# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask import render_template, request, jsonify, session, url_for, redirect, flash
from flask.views import MethodView, View
from app.auth.forms import LoginFrom
from flask_login import login_user
from app.auth.models import User
from sqlalchemy import func


class LoginView(MethodView):

    def get(self):
        form = LoginFrom()
        return render_template("auth/login.html")

    def post(self):
        form = LoginFrom()
        username = form.data['username']
        password = form.data['password']
        user = User.query.filter_by(user_name=func.binary(username)).first()
        if user:
            if user.verify_password(password):
                login_user(user, form.data['rememberme'])
                session['username'] = username
                return redirect(url_for("home.index"))
            flash("用户密码不正确")
            return render_template("auth/login.html")
        flash("用户不存在")
        return render_template("auth/login.html")