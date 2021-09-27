from flask import Blueprint, request
from flask_restx import Api, Resource
import bcrypt, jwt, datetime
from app.models import db, User

bp = Blueprint('auth', __name__)
api = Api(bp)

@api.route('')
class AuthToken(Resource):
    def post(self):
        """Authentication for generate token to user"""
        try:
            # Type check
            username = request.json.get('username')
            password = request.json.get('password')
            if (username is None) or (password is None):
                return {
                    "message": "Required username and password"
                }, 400
            # Query
            user = User.query.filter_by(username=username).first()
            if user is None:
                return {
                    "message": "Invalid username"
                }, 403
            elif not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return {
                    "message": "Invalid password"
                }, 403
            # return token
            return {
                "message": "Sign in {username}",
                "token": generate_jwt(username)
            }, 201
        except Exception as error:
            print(error)
            return {
                "message": "Internal Server Error",
            }, 500

def generate_jwt(username):
    now = datetime.datetime.now()
    payload = {
        "iss": "Samsung Electronics",
        "sub": f"authorized {username}",
        "aud": username,
        "exp": (now + datetime.timedelta(hours=1)).timestamp(),
        "iat": now.timestamp()
    }
    return jwt.encode(payload, "secret", algorithm='HS256')