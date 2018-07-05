# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/7/7 10:30
"""

from flask import Blueprint

weeklyreport = Blueprint('weeklyreport', __name__, template_folder='templates',
                 static_folder='static', url_prefix="/weeklyreport")
from app.weeklyreport import urls, views, models
