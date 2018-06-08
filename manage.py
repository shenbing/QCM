# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from app import create_app

app = create_app()

app.run(debug=True)