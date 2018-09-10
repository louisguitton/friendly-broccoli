from datetime import datetime
from flask import current_app
from flask_login import UserMixin
import boto3
from botocore.errorfactory import ClientError

from app import db, ma, login

s3_client = boto3.client('s3')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class MarshmallowMixin(object):
    def to_dict(self):
        return self.__schema__().dump(self).data

    @classmethod
    def from_dict(cls, d):
        return cls.__schema__().load(d).data


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.Integer, index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(128), index=True)
    nickname = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    location = db.Column(db.String(128), index=True)
    linkedin_url = db.Column(db.String(128), index=True, unique=True)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    picture = db.Column(db.String(128))
    headline = db.Column(db.Text())
    industry = db.Column(db.Text())
    summary = db.Column(db.Text())

    videos = db.relationship('Video', backref='applicant', lazy='dynamic')
    submissions = db.relationship('Submission', backref='applicant', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.linkedin_url)


submission_questions = db.Table(
    'submission_questions',
    db.Column('submission_id', db.Integer, db.ForeignKey('submission.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    length_in_sec = db.Column(db.Integer, default=30)
    order_pos = db.Column(db.Integer, unique=True)

    videos = db.relationship('Video', backref='question', lazy='dynamic')
    # Many to Many relationship between questions and submissions
    submissions = db.relationship(
        'Submission', secondary=submission_questions,
        primaryjoin=(submission_questions.c.question_id == id),
        secondaryjoin=(submission_questions.c.submission_id == id),
        backref=db.backref('questions', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.text)


class Video(db.Model, MarshmallowMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    s3_key = db.Column(db.String(140), index=True, unique=True)
    user_agent = db.Column(db.JSON)

    '''
    duration
    size
    '''

    def __repr__(self):
        return '<Video {}>'.format(self.s3_key)

    def head(self):
        return s3_client.head_object(
            Bucket=current_app.config["S3"]["S3_BUCKET"],
            Key=self.s3_key
            )

    @property
    def file_exists(self):
        try:
            self.head()
            return True
        except ClientError:
            return False


class Submission(db.Model, MarshmallowMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    videos = db.relationship('Video', backref='submission', lazy='dynamic')
    personality = db.Column(db.JSON)

    def __repr__(self):
        return '<Submission ({}, {})>'.format(self.user_id, self.creation_date)


class UserAgentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('platform', 'browser', 'version', 'language')

class PersonalitySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('extraversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness')


class BaseSchema(ma.ModelSchema):
    class Meta:
        sqla_session = db.session

class VideoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Video

Video.__schema__ = VideoSchema

class SubmissionSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Submission

Submission.__schema__ = SubmissionSchema
