import os
from dotenv import load_dotenv
load_dotenv()


# Grabs the folder where the script runs.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Connect to the database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(BASEDIR, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Customise site
SITE_TITLE = "1024 GERMANY"
COMPANY = "Imagine Foundation"

global_data = {
    "VIDEOS": [{
        "question": "Why are you interested in the position?",
        "limit": 90,
        "required": True
    }, {
        "question": "What inspires you the most, and why?",
        "limit": 120,
        "required": True
    }],
}
