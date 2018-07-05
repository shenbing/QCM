# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: __init__.py
@time: 2018/6/8 14:30
"""

from app import db, login_manager
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin, current_user
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

ORGANIZATIONS = (
    '质量中心',
    '软件测试部',
)

userstoroles = db.Table('users_roles', db.Column('id', db.Integer(), primary_key=True),
                        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
                        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')))


class Permission:
    WEEKLY_REPORT_READ = 1
    WEEKLY_REPORT_WRITE = 2
    ADMIN = 1024


class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer(), primary_key=True)
    organization_name = db.Column(db.String(10), nullable=False, unique=True)
    organization_code = db.Column(db.String(10), nullable=True, unique=True)
    create_time = db.Column(db.TIMESTAMP(), default=datetime.now)
    update_time = db.Column(db.TIMESTAMP(), default=datetime.now)
    users = db.relationship('User', backref='organization', lazy='dynamic')

    @staticmethod
    def insert_organizations():
        for org in ORGANIZATIONS:
            if not Organization.query.filter_by(organization_name=org).first():
                org = Organization(organization_name=org)
                db.session.add(org)
                db.session.commit()

    def __str__(self):
        return '<Organization %r>' % self.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(50), nullable=True, unique=True)
    role_permissions = db.Column(db.Integer())
    create_time = db.Column(db.TIMESTAMP(), default=datetime.now)
    update_time = db.Column(db.TIMESTAMP(), default=datetime.now)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.role_permissions is None:
            self.role_permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'EMPLOYEE': [Permission.WEEKLY_REPORT_READ, Permission.WEEKLY_REPORT_WRITE],
            'MANAGER': [Permission.WEEKLY_REPORT_READ, Permission.WEEKLY_REPORT_WRITE],
            'ADMINISTRATOR': [Permission.WEEKLY_REPORT_READ, Permission.WEEKLY_REPORT_WRITE, Permission.ADMIN],
        }
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.role_permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.role_permissions -= perm

    def reset_permissions(self):
        self.role_permissions = 0

    def has_permission(self, perm):
        return self.role_permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    password_md5 = db.Column(db.String(50), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    organization_id = db.Column(db.Integer(), db.ForeignKey('organizations.id'))
    admin_flag = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.TIMESTAMP(), default=datetime.now)
    update_time = db.Column(db.TIMESTAMP(), default=datetime.now)
    roles = db.relationship('Role', secondary=userstoroles,
                            backref=db.backref('users', lazy='joined'), lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_md5 = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password_md5 == hashlib.md5(password.encode(encoding='utf-8')).hexdigest()

    def can(self, permisson):
        if current_user.is_admin:
            return True
        for role in self.roles:
            if role.has_permission(permisson):
                return True
        return False

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    @property
    def is_admin(self):
        if self.admin_flag:
            return True
        for role in self.roles.all():
            if role.role_name == 'ADMINISTRATOR':
                return True
        return False

    def __str__(self):
        return '<User %r>' % self.user_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
