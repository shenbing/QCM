# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SelectField, BooleanField


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('用户名', [validators.DataRequired('用户名为必填项'),
                                   validators.Length(min=4, max=16, message='用户名长度在4-16位')],
                           render_kw={'placeholder': '用户名'})
    password = PasswordField('密码',
                             [validators.DataRequired('密码为必填项'), validators.Length(min=6, max=16, message='密码长度6-16位')],
                             render_kw={'placeholder': '密码'})
    rememberme = BooleanField('保持登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', [validators.DataRequired('用户名为必填项'),
                                   validators.Length(min=4, max=16, message='用户名长度在4-16位')],
                           render_kw={'placeholder': '用户名'})
    password = PasswordField('密码',
                             [validators.DataRequired('密码为必填项'), validators.Length(min=6, max=16, message='密码长度6-16位')],
                             render_kw={'placeholder': '密码'})
    name = StringField('姓名', [validators.DataRequired('姓名为必填项'), validators.Length(min=2, max=10, message='姓名长度2-10位')],
                       render_kw={'placeholder': '姓名'})
    email = StringField('邮箱', [validators.DataRequired('邮箱为必填项'), validators.email('邮箱地址非法')],
                        render_kw={'placeholder': '邮箱'})
