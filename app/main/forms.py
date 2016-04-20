# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length


class LoginForm(Form):
    # 登陆表单
    name = StringField('Username', validators=[Required(), Length(1, 32)])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')
