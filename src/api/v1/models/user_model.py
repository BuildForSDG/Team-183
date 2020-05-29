# third-party imports
from flask_restx import fields, Namespace

auth_ns = Namespace(
    'auth',
    description='Authentication',
    path="/api/v1/users"
)

register_model = auth_ns.model(
    'register_user', {

        'username': fields.String(
            required=True, description='username', example='johndoe'),
        'email': fields.String(
            required=True, description='email address',
            example='johndoe@gmail.com'),
        'password': fields.String(
            required=True, description='password', example='johndoe123'),
        'confirm': fields.String(
            required=True, description='password', example='johndoe123')
    })

login_model = auth_ns.model(
    'login_user', {

        'email': fields.String(
            required=True, description='email address',
            example='johndoe@gmail.com'),
        'password': fields.String(
            required=True, description='password', example='johndoe123')
    })
