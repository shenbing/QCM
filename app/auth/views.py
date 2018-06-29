# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask import render_template, request, jsonify, session, url_for, redirect, flash
from flask.views import MethodView, View
from app.auth.forms import LoginForm, RegisterForm, ProfileForm
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.models import User
from sqlalchemy import func
from ..auth.models import db
from .models import Role
from datetime import datetime


class LoginView(MethodView):

    def get(self):
        form = LoginForm()
        return render_template("auth/login.html")

    def post(self):
        form = LoginForm()
        if not form.validate_on_submit():
            flash(form.errors.popitem()[1][0])
            return render_template("auth/login.html")
        username = form.data['username']
        password = form.data['password']
        user = User.query.filter_by(user_name=func.binary(username)).first()
        if user:
            if user.verify_password(password):
                login_user(user, form.data['rememberme'])
                # session['username'] = username
                return redirect(url_for("home.index"))
            flash("用户密码不正确")
            return render_template("auth/login.html")
        flash("用户不存在")
        return render_template("auth/login.html")


class LogoutView(MethodView):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for("auth.login"))


class RegisterView(MethodView):

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.data['username']
            user = User.query.filter_by(user_name=func.binary(username)).first()
            if user:
                flash("账号已注册")
                return render_template("auth/login.html")
            registeruser = User(
                user_name=form.username.data,
                password=form.password.data,
                real_name=form.name.data,
                email=form.email.data,
                roles=[Role.query.filter_by(role_name='EMPLOYEE').first()])
            db.session.add(registeruser)
            db.session.commit()
            login_user(registeruser, False)
            return redirect(url_for("home.index"))
        else:
            flash(form.errors.popitem()[1][0])
            return render_template("auth/login.html")

class ProfileView(MethodView):
    @login_required
    def get(self):
        form = ProfileForm()
        user = User.query.filter_by(user_name=func.binary(current_user.user_name)).first()
        form.username.data = current_user.user_name
        # form.password.data = user.password
        form.name.data =  user.real_name
        form.email.data = user.email
        form.rolename.data = ','.join([role.role_name for role in user.roles])
        return render_template("auth/profile.html", form = form)

    @login_required
    def post(self):
        form = ProfileForm()
        if form.validate_on_submit():
            username = form.data['username']
            user = User.query.filter_by(user_name=func.binary(username)).first()
            user.email = form.email.data
            user.password = form.password.data
            user.real_name = form.name.data
            user.update_time = datetime.now()
            db.session.add(user)
            db.session.commit()
            flash("个人资料修改成功！")
        else:
            flash(form.errors.popitem()[1][0])
        return render_template("auth/profile.html", form=form)
