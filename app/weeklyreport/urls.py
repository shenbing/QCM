# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from app.weeklyreport.views import *
from app.weeklyreport import weeklyreport

weeklyreport.add_url_rule('weeklyreports',view_func=WeeklyReportView.as_view('weeklyreports'))
weeklyreport.add_url_rule('weeklyreport/write',view_func=WeeklyReportWriteView.as_view('weeklyreportwrite'))