# third-party imports
from flask_restx import reqparse
import werkzeug


register_parser = reqparse.RequestParser()

register_parser.add_argument(
    'username', required=True, help='username should be a string')
register_parser.add_argument(
    'email', required=True, help='email should be a string')
register_parser.add_argument(
    'password', required=True, help='password should be a string')
register_parser.add_argument(
    'confirm', required=True, help='password should be a string')

login_parser = register_parser.copy()
login_parser.remove_argument('username')
login_parser.remove_argument('confirm')

forgot_password_parser = login_parser.copy()
forgot_password_parser.remove_argument('password')

reset_parser = register_parser.copy()
reset_parser.remove_argument('username')


profile_parser = reqparse.RequestParser()
profile_parser.add_argument(
    'email', required=True, help='email should be a string')
# profile_parser.add_argument(
#     'username', required=True, help='username should be a string')
profile_parser.add_argument(
    'first_name', required=True, help='first_name should be a string')
profile_parser.add_argument(
    'last_name', required=True, help='last_name should be a string')
profile_parser.add_argument(
    'phone_number', required=True, help='phone_number should be a string')
profile_parser.add_argument(
    'address', required=True, help='address should be a string')

profile_parser.add_argument(
    'city', required=True, help='city should be a string')
profile_parser.add_argument(
    'country', required=True, help='country should be a string')
profile_parser.add_argument(
    'postal_code', required=True, help='postal_code should be a string')
profile_parser.add_argument(
    'bio', required=True, help='bio should be a string')

profile_parser.add_argument(
    'is_farmer', required=True, help='is_farmer should be a boolean')
profile_parser.add_argument(
    'is_vendor', required=True, help='is_vendor should be a boolean')

profile_parser.add_argument(
    'image_url', required=False, help='upload_file should be a string')
profile_parser.add_argument(
    'image',
    required=False,
    type=werkzeug.datastructures.FileStorage,
    location='files'
    )
