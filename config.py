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
        "S3_KEY": os.environ.get("S3_KEY"),
        "S3_SECRET": os.environ.get("S3_SECRET_ACCESS_KEY"),
        "S3_LOCATION": 'http://{}.s3.amazonaws.com/'.format(os.environ.get("S3_BUCKET"))
    }

    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL')
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'
    AUTH0_NON_INTERACTIVE_CLIENT_ID = os.environ.get('AUTH0_NON_INTERACTIVE_CLIENT_ID')
    AUTH0_NON_INTERACTIVE_CLIENT_SECRET = os.environ.get('AUTH0_NON_INTERACTIVE_CLIENT_SECRET')

    ALLOWED_EXTENSIONS = set(['webm', 'mp4'])

    GLOBAL_DATA = {
        "VIDEOS": [
            {
                "question": "Tell me something about yourself.",
                "limit": 30
            }, 
            {
                "question": "Explain how you interact with colleagues.",
                "limit": 30
            }, 
            {
                "question": "Describe a conflict resolution situation you experienced.",
                "limit": 30
            }, 
            {
                "question": "How do you face a situation requiring skills you don’t have?",
                "limit": 30
            }, 
            {
                "question": "Do you do anything for fun?",
                "limit": 30
            }, 
            {
                "question": "Describe your working habits.",
                "limit": 30
            }
        ],
    }
