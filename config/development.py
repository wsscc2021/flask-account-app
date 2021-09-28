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