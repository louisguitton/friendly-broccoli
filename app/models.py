from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    location = db.Column(db.String(120), index=True)
    linkedin_handle = db.Column(db.String(64), index=True, unique=True)
    # password_hash = db.Column(db.String(128))
    # cv
    # projects as another table

    videos = db.relationship('Video', backref='applicant', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)    


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))

    videos = db.relationship('Video', backref='question', lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.text)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    url = db.Column(db.String(140), index=True, unique=True)

    '''
    has_audio
    has_video
    max_duration
    duration
    size
    device_id
    '''

    def __repr__(self):
        return '<Video {}>'.format(self.url)


'''
# Submission
submission_id
user_id
creation_date (beginning of session)
submission_date (end of session)
state (0, 1, 2, 3)
videos = array of video_id

# Device
user_agent
browser
version%  
'''
