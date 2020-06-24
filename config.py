import os
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY  = os.urandom(12)
    SESSSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SECRET_KEY  = os.urandom(12)
    SESSSION_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True
    ENV = 'tesing'
    SESSSION_COOKIE_SECURE = False