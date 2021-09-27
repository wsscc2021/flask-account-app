from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# database model
class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    def __init__(self, username, password):
        self.username = username
        self.password = password