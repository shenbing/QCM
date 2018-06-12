# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask import render_template, request, jsonify, session
from flask.views import MethodView, View
from app.auth.forms import LoginFrom
from flask_login import login_user
from app.auth.models import User
from sqlalchemy import func


class LoginView(MethodView):
    def get(self):
        form = LoginFrom()
        return render_template("auth/login.html", form=form)

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        if username is None:
            return jsonify({'msg': u'用户名没有输入', 'code': 33, 'data': ''})
        if password is None:
            return jsonify({'msg': u'密码没有输入', 'code': 34, 'data': ''})
        user = User.query.filter_by(user_name=func.binary(username)).first()
        if user:
            if user.verify_password(password):
                login_user(user, data['remember_me'])
                session['username'] = username
                return jsonify({'msg': u'登录成功！', 'code': 200, 'data': ''})
            return jsonify({'msg': u'密码错误', 'code': 36, 'data': ''})
        return jsonify({'msg': u'用户不存在', 'code': 37, 'data': ''})
