# Built-in modules
from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    # Configuration
    app.config.from_envvar('APP_CONFIG_FILE')
    # Blueprint
    from app.services import auth
    from app.services import account
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(account.bp, url_prefix='/account')
    # SQLAlchemy
    from app.models import db
    db.init_app(app)
    return app