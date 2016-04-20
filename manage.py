# -*- coding:utf-8 -*-
from app import create_app, db
from app.models import User, Online, OnlineLog
from flask.ext.script import Manager, Shell


app = create_app('default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Online=Online, OnlineLog=OnlineLog)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
