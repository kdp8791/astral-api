class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'b80a036d617229af9f32dde36eb420c58378eea1f3a56955'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    MONGO_USERNAME = 'astral'
    MONGO_PASSWORD = 'astral'
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'astral'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''
