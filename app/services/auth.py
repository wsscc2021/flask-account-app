# Standard library
import datetime
import jsonschema
import json
import os
# Thrid-party library
from flask import Blueprint, request
from flask_restx import Api, Resource
import bcrypt
import jwt
# Application module
from app import db
from app.models.account import Account

# Blueprint
bp = Blueprint('auth', __name__)
api = Api(bp)

# JsonSchema
schema_file = os.path.join(bp.root_path, "schemas", "auth.json")
with open(schema_file) as f:
    base_schema = json.load(f)

# JsonSchema Decorator
def json_validate(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                if not request.is_json:
                    raise jsonschema.ValidationError("Must be json format")
                jsonschema.validate(request.json, schema)
                return func(*args, **kwargs)
            except jsonschema.ValidationError as error:
                return {
                    "message": error.message
                }, 400
            except jsonschema.SchemaError as error:
                return {
                    "message": "Internal Server error"
                }, 500
        return wrapper
    return decorator

# Business Logic
@api.route('')
class AuthToken(Resource):

    @json_validate(base_schema['post'])
    def post(self):
        """Authentication for generate token to user"""
        try:
            username = request.json.get('username')
            password = request.json.get('password')
            # Query
            account = Account.query.filter_by(username=username).first()
            if account is None:
                return {
                    "message": "Invalid username"
                }, 403
            elif not bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8')):
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