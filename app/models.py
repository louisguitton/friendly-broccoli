# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
from app import db

# engine = create_engine('sqlite:///database.db', echo=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

# Set your classes here.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    location = db.Column(db.String(120), index=True)
    linkedin_handle = db.Column(db.String(64), index=True, unique=True)
    # password_hash = db.Column(db.String(128))
    # cv
    # projects as another table

    def __repr__(self):
        return '<User {}>'.format(self.name)    

'''
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
'''

'''
# Video
video_id
user_id
question_id
date
S3_url
has_audio
has_video
max_duration
duration
size
device_id

# Submission
submission_id
user_id
creation_date (beginning of session)
submission_date (end of session)
state (0, 1, 2, 3)
videos = array of video_id

# Question
question_id
text

# Device
user_agent
browser
version%  
'''


# Create tables.
# Base.metadata.create_all(bind=engine)

