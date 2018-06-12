# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static')
from app.auth import urls, views, models
