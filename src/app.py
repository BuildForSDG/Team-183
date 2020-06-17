"""
    Application versioning
    Main Application Product Point
"""
__version__ = '0.1.0'
# local imports
from src.api.v1 import api_v1_blueprint as v1
from instance.config import app_config

# third-party imports
from flask import Flask, jsonify


def create_app(config_name):
    """Enables having instances of the
    application with different settings
    """

    # initializing the app
    app = Flask(__name__)

    app.config.from_object(app_config[config_name])

    # registering the blueprint
    app.register_blueprint(v1)

    @app.errorhandler(400)
    def bad_req(e):
        return 'Bad request. Please review the request'

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(
            message='please try another page.',
            error='could not find requested data'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(
            message='Sorry! Something went wrong. Try another time',
            error='SERVER DOWN'), 500

    return app
