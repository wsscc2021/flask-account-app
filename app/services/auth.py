from flask import Blueprint
from flask_restx import Api, Resource
from app.models import db, User

bp = Blueprint('auth', __name__)
api = Api(bp)

@api.route('')
class AuthToken(Resource):
    def post(self):
        """Authentication for generate token to user"""
        return {
            "message": "This is auth page!"
        }