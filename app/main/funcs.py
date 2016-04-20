# -*- coding:utf-8 -*-
from flask import session
from flask.ext.login import logout_user
from datetime import datetime
from user_agents import parse

from ..models import Online, OnlineLog
from .. import db


def verify_session():
    # 会话校验，如果当前会话不在服务端数据库中，则登出当前用户
    current_session_info = session.get('lgsess')
    result = Online.query.filter_by(lgsess=current_session_info).first()
    log = OnlineLog.query.filter_by(lgsess=current_session_info).first()
    if result is None:
        logout_user()
    else:
        result.last_active = datetime.utcnow()
        log.last_active = datetime.utcnow()
        db.session.add(result)
        db.session.add(log)
        db.session.commit()


def parse_ua(ua):
    # User-Agent 阅读优化
    return str(parse(ua))
