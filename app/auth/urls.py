# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from app.auth.views import *
from app.auth import auth

auth.add_url_rule('/login',view_func=LoginView.as_view('login'))