from decouple import config

JWT_SECRET_KEY = config('JWT_SECRET_KEY')
FLASK_ENV = config('FLASK_ENV')

MONGO_DBNAME = config('MONGO_DBNAME')
MONGO_URI = config('MONGO_URI')
# TEST_DB_URL = config('MONGO_URI_TEST')
# DEV_DB_URL = config('MONGO_URI_DEV')
# PROD_DB_URL = config('MONGO_URI_PROD')
