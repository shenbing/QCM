# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from app.bug.views import *
from app.bug import bug

bug.add_url_rule('bugsPerDay',view_func=BugsPerDayView.as_view('bugsPerDay'))
bug.add_url_rule('bugsStatus',view_func=BugsStatusView.as_view('bugsStatus'))