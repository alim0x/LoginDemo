# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    # 用户资料模型，用户id，用户名，密码hash值
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Online(db.Model):
    # 在线会话模型，用户id，会话id，UA，ip地址，最后活跃时间
    __tablename__ = 'online_session'
    id = db.Column(db.Integer)
    lgsess = db.Column(db.String(36), primary_key=True)
    useragent = db.Column(db.String(256))
    ip_addr = db.Column(db.String(16))
    last_active = db.Column(db.DateTime)


class OnlineLog(db.Model):
    __tablename__ = 'login_history'
    id = db.Column(db.Integer)
    lgsess = db.Column(db.String(36), primary_key=True)
    useragent = db.Column(db.String(256))
    ip_addr = db.Column(db.String(16))
    last_active = db.Column(db.DateTime)


@login_manager.user_loader
def load_user(user_id):
    # 加载用户回调，找到返回用户对象，否则返回None
    return User.query.get(int(user_id))
