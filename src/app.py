# local imports
from . import create_app

from decouple import config


config_name = config("FLASK_ENV")
app = create_app(config_name=config_name)


def runserver():
    global app
    app.run(port="8084")
