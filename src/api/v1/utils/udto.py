# third-party imports
from flask_restx import reqparse


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
