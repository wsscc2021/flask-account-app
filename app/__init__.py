# Third-party library
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_mail import Mail

# Extensions
db = SQLAlchemy()
redis_client = FlaskRedis()
mail = Mail()

def create_app() -> Flask:
    app = Flask(__name__)
    # Configuration
    app.config.from_envvar('APP_CONFIG_FILE')
    # Blueprint
    from app.services import auth
    from app.services import account
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(account.bp, url_prefix='/account')
    # Extensions init
    db.init_app(app)
    redis_client.init_app(app)
    mail.init_app(app)
    return app