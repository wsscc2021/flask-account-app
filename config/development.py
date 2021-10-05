ENV = "development"
DEBUG = True
TESTING = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{name}?charset=utf8".format(**{
    "username": "dbuser",
    "password": "dbpassword",
    "host": "127.0.0.1",
    "port": 3306,
    "name": "db"
})
REDIS_URL = "redis://{host}:{port}/?charset=utf-8&decode_responses=True".format(**{
    "host": "127.0.0.1",
    "port": 6379
})
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USERNAME = "worldskills.developer@gmail.com"
MAIL_PASSWORD = "zybjjhglqsjuiqas"
MAIL_USE_TLS = False
MAIL_USE_SSL = True