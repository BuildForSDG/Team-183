# config.py

# import os
from decouple import config


class Config(object):

    """Parent configuration class."""

    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    ERROR_404_HELP = False

    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = config('MAIL_PORT')
    MAIL_DEFAULT_SENDER = config('Admin', 'GMAIL_MAIL')
    MAIL_USERNAME = config('GMAIL_USERNAME')
    MAIL_PASSWORD = config('GMAIL_PASSWORD')
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_SUPPRESS_SEND = True


class DevelopmentConfig(Config):

    """Configurations for Development."""

    DEBUG = True
    MODE = "development"
    # DATABASE_URL = config("MONGO_URI_DEV")
    MONGO_URI = config("MONGO_URI_DEV")


class TestingConfig(Config):

    """Configurations for Testing, with a separate test database."""

    TESTING = True
    DEBUG = True
    MODE = "testing"
    # DATABASE_URL = config("TEST_DB_URL")
    MONGO_URI = config("MONGO_URI_TEST")


class ProductionConfig(Config):

    """Configurations for Production."""
    DEBUG = False
    # DATABASE_URL = config("PROD_DB_URL")
    MONGO_URI = config("MONGO_URI_PROD")


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
