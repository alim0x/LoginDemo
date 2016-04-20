# -*- coding:utf-8 -*-
# 配置信息


class Config:
    SECRET_KEY = 'loginddemo'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://---'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://---'


config = {
    'developmemt': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
