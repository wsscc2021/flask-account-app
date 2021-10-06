# Stamdard library
import json
import os
import jsonschema
# Thrid-party library
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
import bcrypt
import random
# Application modules
from app import db
from app import redis_client
from app import mail
from app.models.account import Account

# Blueprint
bp = Blueprint('account', __name__)
api = Api(bp)

# JsonSchema load from jsonfile
def get_schema(filename):
    schema_file = os.path.join(bp.root_path, "schemas", filename)
    with open(schema_file) as f:
        schema = json.load(f)
    return schema

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

# JsonSchema
schema = dict()
schema["account"] = get_schema("account.json")
schema["account_activation_flag"] = get_schema("account_activation_flag.json")

# Business Logic
@api.route('/<username>')
class AccountApi(Resource):

    @json_validate(schema["account"]['post'])
    def post(self,username):
        """Create account"""
        try:
            password = request.json.get('password')
            email = request.json.get('email')
            account = Account(
                username=username,
                password=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8'),
                email=email)
            db.session.add(account)
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
            account = Account.query.filter_by(username=username).first()
            if account:
                db.session.delete(account)
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

    @json_validate(schema["account"]['put'])
    def put(self,username):
        """Updated account"""
        try:
            email = request.json.get('email')
            account = Account.query.filter_by(username=username).first()
            if account:
                account.email = email if email else account.email
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
            account = Account.query.filter_by(username=username).first()
            if account:
                account_attributes = {
                    column.name: str(getattr(account, column.name))
                        for column in account.__table__.columns
                        if column.name not in ['password','id']
                }
                return {
                    "message": "Getting account",
                    "account": account_attributes
                }, 200
            else:
                return {
                    "message": f"{username} does not exists"
                }, 404
        except Exception as error:
            return {
                "message": "Internal Server Error"
            }, 500



@api.route('/<username>/verification_code')
class AccountVerificationCode(Resource):

    def post(self, username):
        try:
            account = Account.query.filter_by(username=username).first()
            if not account:
                return {
                    "message": f"{username} does not exists"
                }, 404

            expire_time = 60 * 10 # 10분
            verification_code_length = 6 # 6자리
            random_int = int(random.random() * (10**verification_code_length))
            verification_code = str(random_int).zfill(verification_code_length) # zfill
            redis_client.set(username, verification_code, ex=expire_time) # redis에 저장

            title = f"{username}님의 인증 코드"
            body = f"인증 코드는 {verification_code} 입니다."
            sender = "worldskills.developer@gmail.com"
            recipients = [account.email]
            message = Message(title, sender=sender, recipients=recipients, body=body)
            mail.send(message)

            return {
                "message": f"Created {username}'s veirfication code"
            }, 201
        except Exception as error:
            return {
                "message": "Internal Server Error"
            }, 500



@api.route('/<username>/activation_flag')
class AccountActivationFlag(Resource):
    
    @json_validate(schema['account_activation_flag']['put'])
    def put(self, username):
        try:
            request_verification_code = request.json.get('verification_code')
            verification_code = redis_client.get(username)
            if request_verification_code != verification_code:
                return {
                    "message": "Invalid Verification code"
                }, 403

            account = Account.query.filter_by(username=username).first()
            if not account:
                return {
                    "message": f"{username} does not exists"
                }, 404

            account.activation_flag = True
            db.session.commit()
            return {
                "message": f"{username} is activated now"
            }
        except Exception as error:
            db.session.rollback()
            return {
                "message": "Internal Server Error"
            }, 500