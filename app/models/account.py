from app import db

# database model
class Account(db.Model):
    __table_name__ = 'account'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    activation_flag = db.Column(db.Boolean(), nullable=False)
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.activation_flag = False