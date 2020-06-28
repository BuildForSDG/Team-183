# local imports
from .app import create_app

# third-party imports
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from decouple import config
from celery import Celery


# application development instance
config_name = config("FLASK_ENV")
app = create_app(config_name=config_name)
app.config.from_pyfile('settings.py')


mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)
mail = Mail(app)
# celery =Celery(app)
# celery = Celery('tasks', broker='amqp://localhost//')
celery = Celery('tasks', broker='amqp://localhost:5672')


# celery_class = celery()
