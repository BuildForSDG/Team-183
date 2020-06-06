# local imports
from ..utils.validators import validate_user_data, validate_reset_user_data
from ..utils.udto import (
    register_parser,
    login_parser,
    forgot_password_parser,
    reset_parser)
from ..utils.mail_services import (
    send_forgot_password_email,
    send_confirm_reset_password_email)
from ..models.user_model import (
    register_model,
    auth_ns,
    login_model,
    forgot_password_model,
    reset_model)

# third-party imports
from flask_restx import Resource
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from decouple import config


@auth_ns.route("/signup")
class RegisterUser(Resource):

    """Registers a new user."""

    @auth_ns.expect(register_model)
    @auth_ns.doc("user registration")
    @auth_ns.response(201, "Created")
    @auth_ns.response(400, "Bad Request")
    def post(self):
        """handles registering a user"""
        new_user = register_parser.parse_args()

        invalid_data = validate_user_data(new_user)
        if invalid_data:
            return invalid_data

        # local import
        from manage import mongo, bcrypt
        users = mongo.db.users
        user = users.find_one({'email': new_user['email']})

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
            "User already exists. Please login or register."}, 200


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

                    return {"warning": "Invalid password"}, 200

                access_token = create_access_token(identity={
                    # 'email': user['email'],
                    # 'email': user['email'],
                    # 'username': user['username'],
                    'email': user['email'],
                })
                return {
                    "message": "Logged in successfully",
                    'token': access_token,
                    # "is_farmer": user["is_farmer"],
                    # "is_restaurant": user["is_farmer"],
                    # "is_vendor": user["is_farmer"],
                }

            return {"warning": "No user found. Please sign up"}, 200
        return {
            "warning": "'username' and 'password' are required fields"}, 200


@auth_ns.route("/forgot-password")
class UserForgotPassword(Resource):

    @auth_ns.expect(forgot_password_model)
    @auth_ns.doc("user forgot password")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Unauthorized")
    def post(self):
        """Sends password reset link to your mail."""
        data = forgot_password_parser.parse_args()
        # data = request.get_json()
        host_url = config('FRONTEND_HOST_DEV') if config(
            'FLASK_ENV') == 'development' else config('FRONTEND_HOST_PROD')
        url = host_url + 'reset'

        # local import
        from manage import mongo
        users = mongo.db.users

        user = users.find_one({'email': data['email']})

        # check if email is taken
        if user and user['email']:

            expires = timedelta(hours=24)
            reset_token = create_access_token(identity={
                'email': user['email'],
            }, expires_delta=expires)

            send_forgot_password_email(
                [user['email']], reset_token, url)

            return {
                'message': 'Email has been sent to ' +
                user['email'] + ' with new password reset link'}, 200

        return {'warning': 'No user exists with that email'}, 409


@auth_ns.route('/reset-password')
class UserResetPassword(Resource):

    "Class for updating user password."

    @auth_ns.expect(reset_model)
    @auth_ns.doc("user reset password")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Unauthorized")
    def put(self):
        """Sends new/updated password to your mail."""
        data = reset_parser.parse_args()
        # data = request.get_json()

        # # local import
        from manage import mongo, bcrypt
        users = mongo.db.users
        user = users.find_one({'email': data['email']})

        invalid_data = validate_reset_user_data(data)
        if invalid_data:
            return invalid_data

        new_password = data['password']
        hash_password = bcrypt.generate_password_hash(
            new_password).decode('utf-8')
        user['password'] = hash_password
        users.save(user)

        send_confirm_reset_password_email(
            [user['email']], new_password)

        return {'message': 'Password updated for ' + \
            user['email'] + '. Check your Email for updated credentials'}, 200
