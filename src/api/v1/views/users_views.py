# local imports
from ..utils.validators import (
    validate_user_data,
    validate_reset_user_data,
    validate_profile_data)
from ..utils.udto import (
    register_parser,
    login_parser,
    forgot_password_parser,
    reset_parser,
    profile_parser)
from ..utils.mail_services import (
    send_forgot_password_email,
    send_confirm_reset_password_email)
from ..models.user_model import (
    register_model,
    auth_ns,
    login_model,
    forgot_password_model,
    reset_model,
    profile_model)
from ..utils.decorators import admin_token_required


# third-party imports
from flask_restx import Resource
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from decouple import config
import cloudinary as Cloud
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import jsonify


Cloud.config.update = ({
    'cloud_name': config('CLOUDINARY_CLOUD_NAME'),
    'api_key': config('CLOUDINARY_API_KEY'),
    'api_secret': config('CLOUDINARY_API_SECRET')
})


# @auth_ns.route("/signup")
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
        from src import mongo, bcrypt
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
                'created': created,
                'profile_completed': False
            })

            new_user = users.find_one({'_id': user_id})

            message = 'User with email ' + \
                new_user['email'] + ' registered successfully'
            return {'message': message}, 201

        return {
            "warning":
            "User already exists. Please login or register."}, 200


# @auth_ns.route("/login")
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
        from src import mongo, bcrypt
        users = mongo.db.users

        if args["email"] and args["password"]:
            user = users.find_one({'email': args['email']})

            if user:

                if not bcrypt.check_password_hash(
                        user['password'], args["password"]):

                    return {"warning": "Invalid password"}, 200

                print (user['profile_completed'])
                if not user['profile_completed']:

                    access_token = create_access_token(
                        identity={
                            'username': user['username'],
                            'email': user['email'],
                            "sub": user['_id'],

                        },
                        # sub=user['_id']
                    )
                    return {
                        "message": "Logged in successfully",
                        'token': access_token,
                        'profile_completed': user['profile_completed'],

                    }

                access_token = create_access_token(
                    identity={

                        'first_name': user['first_name'],
                        'last_name': user['last_name'],
                        'username': user['username'],
                        'email': user['email'],

                        'phone_number': user['phone_number'],
                        'address': user['address'],
                        'city': user['city'],
                        'country': user['country'],
                        'postal_code': user['postal_code'],

                        'bio': user['bio'],
                        'image_url': user['image_url'],

                        'is_farmer': user['is_farmer'],
                        'is_vendor': user['is_vendor'],
                        'profile_completed': user['profile_completed'],
                        "sub": user['_id']
                    },
                    # sub=user['_id']
                )

                return {
                    "message": "Logged in successfully",
                    'token': access_token,
                    'profile_completed': user['profile_completed'],

                    'admin': user['is_vendor'],

                }

            return {"warning": "No user found. Please sign up"}, 200
        return {
            "warning": "'username' and 'password' are required fields"}, 200


# @auth_ns.route("/forgot-password")
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
        from src import mongo
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

        return {'warning': 'No user exists with that email'}, 200


# @auth_ns.route('/reset-password')
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
        from src import mongo, bcrypt
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

        return {'message': 'Password updated for ' +
                user['email'] + '. Check your Email for updated credentials'}, 200


# @auth_ns.route("/profile")
class LoggedInUserProfile(Resource):

    "Class for display and edit a logged in user profile"

    @auth_ns.expect(profile_model)
    @auth_ns.doc("user profile")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Unauthorized")
    def patch(self):
        """Handles editing a logged in user profile."""
        user_profile = profile_parser.parse_args()
        # file_to_upload = ''
        file_to_upload = user_profile['image']
        # print(file_to_upload)

        invalid_data = validate_profile_data(user_profile)
        if invalid_data:
            return invalid_data

        # local import
        from src import mongo
        users = mongo.db.users
        user = users.find_one({'email': user_profile['email']})

        if user:

            thumbnail_url = 'https://res.cloudinary.com/daniel2019/image/upload/c_fill,h_100,w_100/lulihiitm8tp4npblsgh.jpg'
            if user_profile['image_url']:
                thumbnail_url = user_profile['image_url']

            if file_to_upload:
                upload_result = upload(file_to_upload)
                thumbnail_url1, options = cloudinary_url(
                    upload_result['public_id'],
                    format="jpg",
                    crop="fill",
                    width=100,
                    height=100)
                thumbnail_url = thumbnail_url1

                thumbnail_url2, options = cloudinary_url(
                    upload_result['public_id'],
                    format="jpg",
                    crop="fill",
                    width=200,
                    height=100,
                    radius=20,
                    effect="sepia")
                thumbnail_pixelate, options = cloudinary_url(
                    upload_result['public_id'],
                    format="jpg",
                    crop="fill",
                    width=200,
                    height=300,
                    radius=20,
                    effect="pixelate_faces:9",
                    gravity="face")

            is_farmer = False
            is_vendor = False
            if user_profile['is_farmer'] == 'True':
                is_farmer = True
            if user_profile['is_vendor'] == 'True':
                is_vendor = True

            user.update({
                'first_name': user_profile['first_name'],
                'last_name': user_profile['last_name'],
                # 'email': user_profile['email'],
                # 'username': user_profile['username'],

                # 'contact_info':
                #     {
                #         'address': user_profile['address'],
                #         'phone_number': user_profile['phone_number'],
                #         'city': user_profile['city'],
                #         'country': user_profile['country'],
                #         'postal_code': user_profile['postal_code'],
                #     },
                'phone_number': user_profile['phone_number'],
                'address': user_profile['address'],
                'city': user_profile['city'],
                'country': user_profile['country'],
                'postal_code': user_profile['postal_code'],

                'bio': user_profile['bio'],
                'image_url': thumbnail_url,

                'is_farmer': is_farmer,
                'is_vendor': is_vendor,
                'profile_completed': True,

                'updated': datetime.utcnow(),

            })

            users.save(user)

            message = 'User with email ' + \
                user_profile['email'] + ' profile updated successfully'
            return {'message': message}, 201

        return {
            "warning":
            "User updated profile already. Please login or register."}, 200


class AllUsers(Resource):
    @auth_ns.response(200, 'Success')
    # @auth_ns.marshal_with(users_resp, envelope='users')
    # @token_required
    @admin_token_required
    @auth_ns.doc(security='apikey')
    @auth_ns.header(
        'token',
        type=str,
        description='access token')
    def get(user_id, self):
        """Gets all users from db."""
        # local import
        from src import mongo
        users = mongo.db.users
        usersx = users.find()

        if not usersx:
            auth_ns.abort(404, "No users for found")

        results = []
        for user in usersx:
            obj = {
                "user_id": str(user["_id"]),
                "email": user["email"],
                "username": user["username"],
                # "admin": user["is_vendor"],
                # "status": user["status"],
                "registered_on": user["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }
            results.append(obj)

        return jsonify(
            {"message": "All users listed successfully",
             "users_count": users.count(),
             "users": results
             })
