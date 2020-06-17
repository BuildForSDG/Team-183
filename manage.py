# local imports
from src import app


# third-party imports
from flask_script import Manager
from decouple import config
import unittest


manager = Manager(app)


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
    # app.run()
    manager.run()
