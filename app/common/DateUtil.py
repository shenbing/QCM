# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: ZentaoParser.py
@time: 2018/6/8 14:30
"""

from datetime import datetime
from datetime import date
from datetime import timedelta
import time


def get_week_count(at=datetime.now()):
    return at.isocalendar()[1]

def get_this_monday():
    today = date.today()
    weekday = today.weekday()
    return today - timedelta(weekday)

def get_special_monday(datetime):
    weekday = datetime.weekday()
    return (datetime - timedelta(weekday)).date()

def get_last_week():
    return datetime.now() - timedelta(days=7)

def get_last_week_start_at():
    return get_this_monday() - timedelta(days=7)

def get_last_week_end_at():
    return get_this_monday()


if __name__ == '__main__':
    import time
    print(get_this_monday())
    print(get_special_monday(datetime.now()))
