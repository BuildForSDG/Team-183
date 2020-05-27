# local imports
from src import create_app


# third-party imports
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
# controller class for handling commands
from flask_script import Manager
from decouple import config
import unittest


# application development instance
config_name = config("FLASK_ENV")
app = create_app(config_name=config_name)
app.config.from_pyfile('settings.py')


mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
manager = Manager(app)
CORS(app)


@manager.command
def runserver():
    port = int(config("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@manager.command
def test():
    test = unittest.TestLoader().discover(
        "./app/tests", pattern="test*.py")
    unittest.TextTestRunner(verbosity=2).run(test)


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
