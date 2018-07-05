# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask import render_template, abort, request, current_app, redirect, url_for, flash
from flask.views import MethodView, View
from flask_login import login_required, current_user
from app.auth.models import Permission, User
from app.weeklyreport.models import WeeklyReport
from app.weeklyreport.forms import WriteForm
from app.common.DateUtil import get_this_monday, get_week_count
from datetime import timedelta, datetime
from app import db


class WeeklyReportView(MethodView):
    @login_required
    def get(self):
        user_id = request.args.get("user_id")
        if current_user.can(Permission.WEEKLY_REPORT_READ):
            if user_id is None or user_id == "all":
                page = request.args.get('page', 1, type=int)
                pagination = WeeklyReport.query.order_by(WeeklyReport.create_time.desc()).paginate(
                    page, per_page=current_app.config['PER_PAGE'],
                    error_out=False)
                return render_template("weeklyreport/weeklyreport.html", user_id=user_id, users=User.query.all(),
                                       pagination=pagination)
            else:
                page = request.args.get('page', 1, type=int)
                pagination = WeeklyReport.query.filter_by(user_id=request.args.get("user_id")).order_by(
                    WeeklyReport.create_time.desc()).paginate(
                    page, per_page=current_app.config['PER_PAGE'],
                    error_out=False)
                return render_template("weeklyreport/weeklyreport.html", user_id=user_id, users=User.query.all(),
                                       pagination=pagination)
        else:
            return redirect(url_for("auth.login"))


class WeeklyReportWriteView(MethodView):
    @login_required
    def get(self):
        if not current_user.can(Permission.WEEKLY_REPORT_WRITE):
            return redirect(url_for("auth.login"))
        form = WriteForm()
        report = WeeklyReport.query.filter_by(user_id=current_user.id, week_count=get_week_count(),
                                              year=datetime.today().year).first()
        if report:
            form.body.data = report.content
        else:
            form.body.data = "<p><b>本周工作内容:</b></p><ol><li></li></ol><p><b>&nbsp;下周计划:</b></p><ol><li></li></ol><p></p>"
        return render_template("weeklyreport/write.html", form=form, week_count=get_week_count(),
                               start_at=get_this_monday(), end_at=get_this_monday() + timedelta(days=6))

    @login_required
    def post(self):
        if not current_user.can(Permission.WEEKLY_REPORT_WRITE):
            return redirect(url_for("auth.login"))
        form = WriteForm()
        report = WeeklyReport.query.filter_by(user_id=current_user.id, week_count=get_week_count(),
                                              year=datetime.today().year).first()
        if form.submit.data and form.validate_on_submit():
            if report:
                report.content = form.body.data.replace('<br>', '')
                db.session.add(report)
            else:
                report = WeeklyReport(content=form.body.data.replace('<br>', ''), user_id=current_user.id,
                                      week_count=get_week_count(), year=datetime.today().year)
                db.session.add(report)
            db.session.commit()
            flash("周报提交成功")
            return redirect(url_for('weeklyreport.weeklyreportwrite'))
        return redirect(url_for("auth.login"))
