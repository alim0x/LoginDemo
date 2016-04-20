# -*- coding:utf-8 -*-
import uuid
from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask import request, flash
from flask.ext.login import login_required, login_user, logout_user

from . import main
from .forms import LoginForm
from .. import db
from ..models import User, Online, OnlineLog
from .funcs import verify_session, parse_ua


@main.before_request
def before_request():
    verify_session()


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 用户校验通过允许登陆
            login_user(user)

            session['name'] = form.name.data
            session['useragent'] = parse_ua(request.headers.get('User-Agent'))
            session['lgsess'] = str(uuid.uuid4())
            uid = User.query.filter_by(username=session.get('name')).first().id
            session['uid'] = uid
            session['ip_addr'] = request.remote_addr

            # 将当前用户会话信息提交到服务端
            session_info = Online(id=uid, lgsess=session.get('lgsess'),
                                  useragent=session.get('useragent'),
                                  ip_addr=session.get('ip_addr'))
            session_log = OnlineLog(id=uid, lgsess=session.get('lgsess'),
                                    useragent=session.get('useragent'),
                                    ip_addr=session.get('ip_addr'))
            db.session.add(session_info)
            db.session.add(session_log)
            db.session.commit()
            return redirect(request.args.get('next') or url_for('main.user',
                            name=session.get('name')))
        flash('Invalid username or password.')
    return render_template('index.html', form=form)


@main.route('/user')
@login_required
def logintmp():
    return redirect(url_for('main.user', name=session.get('name')))


@main.route('/user/<name>')
@login_required
def user(name):
    # 查询所有在线会话信息
    online_sessions = Online.query.filter_by(id=session.get('uid')).all()
    cur_sessions = []
    # 移除10分钟以上未活动会话
    for s in online_sessions:
        if (datetime.utcnow() - s.last_active).seconds > 600:
            db.session.delete(s)
            db.session.commit()
        else:
            cur_sessions.append(s)
    return render_template('user.html', name=name, sessions=cur_sessions,
                           sid=session.get('lgsess'))


@main.route('/user/<name>/log')
@login_required
def login_history(name):
    # 查询所有历史会话信息
    history_sessions = OnlineLog.query.filter_by(id=session.get('uid')).all()
    return render_template('log.html', name=name, sessions=history_sessions,
                           sid=session.get('lgsess'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    # 登出用户并删除对应会话信息
    session_info = Online.query.filter_by(lgsess=session.get('lgsess')).first()
    db.session.delete(session_info)
    db.session.commit()
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/logout/<sid>')
@login_required
def logout_sid(sid):
    # 登出指定会话
    s = Online.query.filter_by(lgsess=sid).first()
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('main.user', name=session.get('name')))
