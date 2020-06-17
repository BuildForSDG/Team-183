"""Application versioning."""
# local imports
from .views.users_views import (
    auth_ns,
    RegisterUser,
    LoginUser,
    UserForgotPassword,
    UserResetPassword,
    LoggedInUserProfile
)


# third-party imports
from flask_restx import Api
from flask import Blueprint


api_v1_blueprint = Blueprint(
    'api',
    __name__,
    # url_prefix='/api/v1',
)

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "token"
    }
}

auth_api = Api(
    api_v1_blueprint,
    version='1.0',
    title='team-183 API',
    authorizations=authorizations,
    description='A team-183 API',
    doc='/'
)


# del auth_api.namespaces[0]
auth_api.add_namespace(auth_ns)

auth_ns.add_resource(RegisterUser, '/signup', endpoint='signup')
auth_ns.add_resource(LoginUser, '/login', endpoint='login')
auth_ns.add_resource(UserForgotPassword, '/forgot-password', endpoint='forgot-password')
auth_ns.add_resource(UserResetPassword, '/reset-password', endpoint='reset-password')
auth_ns.add_resource(LoggedInUserProfile, '/profile', endpoint='profile')
