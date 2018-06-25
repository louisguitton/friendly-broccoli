import os

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
    "FIELDS": [{
        "label": "Your Name",
        "name": "name",
        "type": "text",
        "placeholder": "",
        "required": True
    }, {
        "label": "Email",
        "name": "email",
        "type": "text",
        "placeholder": "",
        "required": True
    }, {
        "label": "Location",
        "name": "location",
        "type": "text",
        "placeholder": "Where are you now?",
        "required": True
    }, {
        "label": "You, on the Web",
        "name": "web",
        "type": "textarea",
        "placeholder": "Any public social links that help us get to know you. (Please put each link on a new line.)",
        "required": True
    }, {
        "label": "Projects",
        "name": "projects",
        "type": "textarea",
        "placeholder": "Any links to projects you've built or worked on. (Please put each link on a new line.)",
        "required": False
    }, {
        "label": "CV",
        "name": "cv",
        "type": "file",
        "placeholder": "Your CV (PDF, DOC, TXT)",
        "required": False
    }]
}
