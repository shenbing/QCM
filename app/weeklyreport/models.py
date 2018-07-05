# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/7/7 14:30
"""

from app import db, login_manager
from flask import current_app
from datetime import datetime
from app.auth.models import User
from app.common.DateUtil import get_week_count, get_last_week

class WeeklyReport(db.Model):
    __tablename__ = 'weeklyreports'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    year = db.Column(db.Integer)
    week_count = db.Column(db.Integer)
    create_time = db.Column(db.TIMESTAMP(), default=datetime.now)
    update_time = db.Column(db.TIMESTAMP(), default=datetime.now)
    user = db.relationship('User', backref='reports', lazy='joined')

    @property
    def is_of_current_week(self):
        if self.week_count == get_week_count() \
                and self.year == datetime.today().year:
            return True
        return False

    @property
    def is_of_last_week(self):
        if self.week_count == get_week_count(get_last_week()) \
                and self.year == get_last_week().year:
            return True
        return False

    def __str__(self):
        return 'Posted by {} at {}'.format(
            User.query.get(self.user_id).email, self.create_time)