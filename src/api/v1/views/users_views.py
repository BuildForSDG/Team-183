# local imports
from ..utils.validators import validate_user_data
from ..utils.udto import register_parser
from ..models.user_model import register_model, auth_ns

# third-party imports
from flask_restx import Resource
from datetime import datetime


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
