# Stamdard library
import json
import os
import jsonschema
# Thrid-party library
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from sqlalchemy.exc import IntegrityError
import bcrypt
# Application modules
from app.models import db, User

# Blueprint
bp = Blueprint('account', __name__)
api = Api(bp)

# JsonSchema
schema_file = os.path.join(bp.root_path, "schemas", "account.json")
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
@api.route('/<username>')
class Account(Resource):

    @json_validate(base_schema['post'])
    def post(self,username):
        """Create account"""
        try:
            password = request.json.get('password')
            email = request.json.get('email')
            user = User(
                username=username,
                password=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8'),
                email=email)
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
        except Exception as error:
            return {
                "message": "Internal Server Error"
            }, 500

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

    @json_validate(base_schema['put'])
    def put(self,username):
        """Updated account"""
        try:
            email = request.json.get('email')
            user = User.query.filter_by(username=username).first()
            if user:
                user.email = email if email else user.email
                db.session.commit()
                return {
                    "message": f"Updated {username}"
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

    def get(self,username):
        """Get account"""
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                user_attributes = {
                    column.name: str(getattr(user, column.name))
                        for column in user.__table__.columns
                        if column.name not in ['password','id']
                }
                return {
                    "message": "Getting account",
                    "user": user_attributes
                }, 200
            else:
                return {
                    "message": f"{username} does not exists"
                }, 404
        except Exception as error:
            return {
                "message": "Internal Server Error"
            }, 500