import os
from dotenv import load_dotenv

# Grabs the folder where the script runs.
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config(object):
    # Enable debug mode.
    DEBUG = True

    # Secret key for session management. You can generate random strings here:
    # https://randomkeygen.com/
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Connect to the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMINS = ['louisguitton93@gmail.com']

    S3 = {
        "S3_BUCKET": os.environ.get("S3_BUCKET"),
        "S3_KEY": os.environ.get("AWS_ACCESS_KEY_ID"),
        "S3_SECRET": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "S3_LOCATION": 'http://{}.s3.amazonaws.com/'.format(os.environ.get("S3_BUCKET")),
        "S3_REGION": os.environ.get("S3_REGION")
    }

    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_CALLBACK_ENDPOINT = os.environ.get('AUTH0_CALLBACK_ENDPOINT')
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'
    AUTH0_NON_INTERACTIVE_CLIENT_ID = os.environ.get('AUTH0_NON_INTERACTIVE_CLIENT_ID')
    AUTH0_NON_INTERACTIVE_CLIENT_SECRET = os.environ.get('AUTH0_NON_INTERACTIVE_CLIENT_SECRET')

    REDIS_HOST = "0.0.0.0"
    REDIS_PORT = 6379
    BROKER_URL = os.environ.get('REDIS_URL', "redis://{host}:{port}/0".format(
        host=REDIS_HOST, port=str(REDIS_PORT)))
    CELERY_RESULT_BACKEND = BROKER_URL

    ALLOWED_EXTENSIONS = set(['webm', 'mp4'])

    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID')

    BETA_MODE_ON = True