from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from sqlalchemy.exc import IntegrityError
import bcrypt
# Application modules
from app.models import db, User

bp = Blueprint('account', __name__)
api = Api(bp)

@api.route('/<username>')
class Account(Resource):
    def post(self,username):
        """Create account"""
        try:
            password = request.json.get('password')
            email = request.json.get('email')
            if password and email:
                user = User(username=username, password=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8'))
                db.session.add(user)
                db.session.commit()
                return {
                    "message": f"Created {username}"
                }, 201
            elif not password:
                return {
                    "message": "Required password"
                }, 400
            elif not email:
                return {
                    "message": "Required email"
                }, 400
        except IntegrityError as error:
            db.session.rollback()
            return {
                "message": "Duplicate username"
            }, 403
    def delete(self,username):
        """Delete account"""
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return {
                    "message": f"Deleted {username}"
                }, 200
            else:
                return {
                    "message": f"{username} does not exists"
                }, 404
        except Exception as error:
            db.session.rollback()
            return {
                "message": "Server Internal Error"
            }, 500
    def put(self):
        """Updated account"""
        return {
            "message": "Updated account"
        }
    def delete(self):
        """Deleted account"""
        return {
            "message": "Deleted account"
        }