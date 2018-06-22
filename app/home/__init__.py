# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask import Blueprint

home = Blueprint('home', __name__, template_folder='templates',
                 static_folder='static', url_prefix="/home")
from app.home import urls, views, models
