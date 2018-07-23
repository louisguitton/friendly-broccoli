from datetime import datetime
from flask_login import UserMixin

from app import db
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.Integer, index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(120), index=True)
    nickname = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    location = db.Column(db.String(120), index=True)
    linkedin_url = db.Column(db.String(64), index=True, unique=True)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    picture = db.Column(db.String(128))
    headline = db.Column(db.Text())
    industry = db.Column(db.Text())
    summary = db.Column(db.Text())

    videos = db.relationship('Video', backref='applicant', lazy='dynamic')
    submissions = db.relationship('Submission', backref='applicant', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.linkedin_url)    


submission_questions = db.Table('submission_questions',
    db.Column('submission_id', db.Integer, db.ForeignKey('submission.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))

    videos = db.relationship('Video', backref='question', lazy='dynamic')
    # Many to Many relationship between questions and submissions
    submissions = db.relationship(
        'Submission', secondary=submission_questions,
        primaryjoin=(submission_questions.c.question_id == id),
        secondaryjoin=(submission_questions.c.submission_id == id),
        backref=db.backref('questions', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.text)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
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
    # state = db.Column
    videos = db.relationship('Video', backref='submission', lazy='dynamic')

    '''
    state (0, 1, 2, 3)
    '''
    def __repr__(self):
        return '<Submission ({}, {})>'.format(self.creation_date, self.submission_date)




'''
# Device
user_agent
browser
version%  
'''
