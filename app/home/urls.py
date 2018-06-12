# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from app.home.views import *
from app.home import home

home.add_url_rule('/',view_func=IndexView.as_view('/'))
home.add_url_rule('/index',view_func=IndexView.as_view('index'))