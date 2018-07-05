# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class WriteForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("提交")
