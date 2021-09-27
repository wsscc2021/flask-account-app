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
            if not password:
                return {
                    "message": "Required password"
                }, 400
            user = User(username=username, password=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8'))
            db.session.add(user)
            db.session.commit()                
            return {
                "message": f"Created {username}"
            }, 201
        except IntegrityError as error:
            db.session.rollback()
            return {
                "message": "Duplicate username"
            }, 403
    def delete(self):
        """Delete account"""
        return {
            "message": "Deleted account"
        }
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