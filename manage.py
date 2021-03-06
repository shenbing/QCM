# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from flask_cli import FlaskCLI
from app import *
from flask_migrate import upgrade, init, migrate as dbmigrate
import click
import os
import sys
import threading
from app.common import threads_function
from app.auth import auth
from app.home import home
from app.bug import bug
from app.weeklyreport import weeklyreport
from app.auth.models import Organization
from app.auth.models import Role
from app.auth.models import User
from app.auth.models import Permission

app = create_app()
FlaskCLI(app)

# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Organization=Organization, Role=Role, Permission=Permission)


# 注册蓝图
app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(bug)
app.register_blueprint(weeklyreport)

COV = None
if app.config.get("COVERAGE"):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Sumary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@app.cli.command()
def deploy():
    # migrate database to latest revision
    # init()
    dbmigrate()
    upgrade()
    # Organization.insert_organizations()
    # Role.insert_roles()
    # admin = User(user_name='administrator', password='666666', real_name='超级管理员', admin_flag = True)
    # db.session.add(admin)
    # db.session.commit()

if __name__ == "__main__":
    t_zentao_info = threading.Thread(target=threads_function.get_zentao_bug_info)
    t_zentao_info.setDaemon(True)
    t_zentao_info.start()
    app.run(host="0.0.0.0", debug=True)
