# local imports
from ..utils.validators import validate_user_data
from ..utils.udto import register_parser, login_parser, forgot_password_parser
from ..models.user_model import (
    register_model, auth_ns,
    login_model,
    forgot_password_model)
from ..utils.helpers import send_forgot_password_email

# third-party imports
from flask_restx import Resource
from datetime import datetime
from flask_jwt_extended import create_access_token
import uuid


@auth_ns.route("/signup")
class UserRegister(Resource):

    """Registers a new user."""

    @auth_ns.expect(register_model)
    @auth_ns.doc("user registration")
    @auth_ns.response(201, "Created")
    @auth_ns.response(400, "Bad Request")
    def post(self):
        """handles registering a user"""
        new_user = register_parser.parse_args()

        # local import
        from manage import mongo, bcrypt
        users = mongo.db.users

        user = users.find_one({'email': new_user['email']})

        invalid_data = validate_user_data(new_user)
        if invalid_data:
            return invalid_data
        if not user:

            username = new_user['username']
            email = new_user['email']
            hash_password = bcrypt.generate_password_hash(
                new_user['password']).decode('utf-8')
            created = datetime.utcnow()

            user_id = users.insert({
                'username': username,
                'email': email,
                'password': hash_password,
                'created': created
            })

            new_user = users.find_one({'_id': user_id})

            message = 'User with email ' + \
                new_user['email'] + ' registered successfully'
            return {'message': message}, 201

        return {
            "warning":
            "User already exists. Please login or register."}, 400


@auth_ns.route("/login")
class LoginUser(Resource):

    "Class for logging in a user"

    @auth_ns.expect(login_model)
    @auth_ns.doc("user login")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Unauthorized")
    def post(self):
        """Handles logging the user."""
        args = login_parser.parse_args()

        # local import
        from manage import mongo, bcrypt
        users = mongo.db.users

        if args["email"] and args["password"]:
            user = users.find_one({'email': args['email']})

            if user:

                if not bcrypt.check_password_hash(
                        user['password'], args["password"]):

                    return {"warning": "Invalid password"}, 400

                access_token = create_access_token(identity={
                    'email': user['email']
                })
                return {
                    "message": "Logged in successfully",
                    'token': access_token,
                    # "admin": user["admin"],
                }

            return {"warning": "No user found. Please sign up"}, 401
        return {
            "warning": "'username' and 'password' are required fields"}, 400


@auth_ns.route("/forgot-password")
class UserForgotPassword(Resource):

    @auth_ns.expect(forgot_password_model)
    @auth_ns.doc("user login")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Unauthorized")
    def post(self):
        """Sends new password to your mail."""
        # data = request.get_json()
        data = forgot_password_parser.parse_args()

        # local import
        from manage import mongo, bcrypt
        users = mongo.db.users

        user = users.find_one({'email': data['email']})

        # check if email is taken
        if user and user['email']:

            new_password = uuid.uuid4().hex.upper()[0:6]
            hash_password = bcrypt.generate_password_hash(
                new_password).decode('utf-8')
            user['password'] = hash_password
            users.save(user)

            send_forgot_password_email([user['email']], new_password)
            return {
                'message': 'Email has been sent with new password'}, 200

        return {'warning': 'No user exists with that email'}, 409
