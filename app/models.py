from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

from app import db
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    location = db.Column(db.String(120), index=True)
    linkedin_handle = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # cv
    # projects as another table

    videos = db.relationship('Video', backref='applicant', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


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



class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    submission_date = db.Column(db.DateTime, index=True)
    state = db.Column

    '''
    state (0, 1, 2, 3)
    videos = array of video_id
    '''
    def __repr__(self):
        return '<Submission ({}, {})>'.format(self.creation_date, self.submission_date)

'''
# Device
user_agent
browser
version%  
'''
