import json
from flask_testing import TestCase
from manage import app
from instance.config import app_config
from manage import mongo


class BaseTestCase(TestCase):

    """Base Tests"""

    @classmethod
    def create_app(cls):
        # app.config.from_object('instance.config.TestingConfig')
        app.config.from_object(app_config['testing'])
        return app

    def setUp(self):
        # self.db = Database(testing="testing")
        self.db = mongo.db.users

        self.user = json.dumps(
            {
                "_id": 1,
                "username": "kamar",
                "email": 'kamardaniel@gmail.com',
                "password": 'password',
                "confirm": 'password',
                # "admin": False
            })

    def tearDown(self):
        self.db.dropDatabase()
