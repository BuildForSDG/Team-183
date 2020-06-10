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

forgot_password_model = auth_ns.model(
    'forgot_password', {

        'email': fields.String(
            required=True, description='email address',
            example='johndoe@gmail.com'),
    })

reset_model = auth_ns.model(
    'reset_user_password', {

        # 'username': fields.String(
        #     required=True, description='username', example='johndoe'),
        'email': fields.String(
            required=True, description='email address',
            example='johndoe@gmail.com'),
        # 'old_password': fields.String(
        #     required=True, description='old_password', example='johndoe123'),
        'password': fields.String(
            required=True, description='password', example='johndoe123'),
        'confirm': fields.String(
            required=True, description='password', example='johndoe123')
    })

profile_model = auth_ns.model(
    'user_profile', {

        'email': fields.String(
            required=True, description='email address',
            example='johndoe@gmail.com'),
        # 'username': fields.String(
        #     required=True, description='username', example='John'),
        'first_name': fields.String(
            required=True, description='first_name', example='John'),
        'last_name': fields.String(
            required=True, description='last_name', example='Doe'),
        'phone_number': fields.String(
            required=True, description='phone_number',
            example='+254-721-102111'),
        'address': fields.String(
            required=True, description='address', example='P.O. Box 123456'),

        'city': fields.String(
            required=True, description='city', example='Nairobi'),
        'country': fields.String(
            required=True, description='country', example='Kenya'),
        'postal_code': fields.String(
            required=True, description='postal_code', example='00100'),
        'bio': fields.String(
            required=True, description='bio', example='I am the worlds greatest software engineer'),

        'is_farmer': fields.Boolean(
            required=True, description='is_farmer', example=True),
        'is_vendor': fields.Boolean(
            required=True, description='is_vendor', example=False),
        'image_url': fields.String(
            required=False, description='upload_file', example='https://res.cloudinary.com/daniel2019/image/upload/c_fill,h_100,w_100/bxij26rdhlr6icynkd3f.jpg'),
    })
