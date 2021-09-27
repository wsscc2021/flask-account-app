class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return "mysql+pymysql://{username}:{password}@{host}:{port}/{name}?charset=utf8".format(**self.DATABASE)

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_ECHO = True
    DATABASE = {
        "username": "dbuser",
        "password": "dbpassword",
        "host": "127.0.0.1",
        "port": 3306,
        "name": "db"
    }

class ProductionConfig(Config):
    ENV = "production"