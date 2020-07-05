from functools import wraps

from flask import request, current_app, jsonify, make_response
import jwt
from ..models.user_model import auth_ns


def token_required(f):
    """Ensures user is logged in before action."""
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None
        user_id = ""
        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            auth_ns.abort(400, "Token Missing")
        try:
            payload = jwt.decode(token, current_app.config.get("JWT_SECRET_KEY"))
            user_id = payload['identity']['sub']

        except jwt.ExpiredSignatureError:
            auth_ns.abort(400, "Token has expired. Please login again")

        except jwt.InvalidTokenError:
            auth_ns.abort(400, "Invalid token")

        return f(user_id, *args, **kwargs)
    return wrap


def admin_token_required(f):
    """Ensures admin user is logged in before action."""
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None
        user_id = ""
        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            auth_ns.abort(400, "Token Missing")
        try:
            payload = jwt.decode(token, current_app.config.get("JWT_SECRET_KEY"))
            user_id = payload['identity']['sub']
            # admin = payload['identity']['is_farmer']
            admin = payload['identity']['is_vendor']
            print(admin)
            if not admin:
                return make_response(jsonify({
                    "message": "Not authorized to perform this function"}),
                    401)

        except jwt.ExpiredSignatureError:
            auth_ns.abort(400, "Token has expired. Please login again")

        except jwt.InvalidTokenError:
            auth_ns.abort(400, "Invalid token")

        return f(user_id, *args, **kwargs)
    return wrap
