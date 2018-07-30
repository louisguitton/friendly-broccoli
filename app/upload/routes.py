from flask import current_app, jsonify, flash, request, render_template
from flask_login import login_required, current_user
import boto3
from botocore.exceptions import ParamValidationError

from app import db
from app.upload import bp
from app.models import User, Question, Video, UserAgentSchema, VideoSchema


s3_client = boto3.client('s3')


@bp.route('/url')
@login_required
def get_signed_url():
    # http://127.0.0.1:5000/upload/url?prefix=bar/baz&key=test.csv&content_type=text/csv
    prefix = request.args.get('prefix', default = '', type = str)
    key = request.args.get('key', default = None, type = str)
    content_type = request.args.get('content_type', default = None, type = str)

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
            'Bucket': current_app.config["S3"]["S3_BUCKET"],
            'Key': "{}/{}".format(prefix, key) if prefix else "{}".format(key),
            'ContentType': content_type,
            })

        return jsonify({"url": url})
    except ParamValidationError:
        return "need more args"


@bp.route('/enqueue')
@login_required
def enqueue_video():
    key = request.args.get('key', default = None, type = str)
    question_id = request.args.get('question_id', default = None, type = int)

    v = Video(
        applicant=current_user._get_current_object(),
        question=Question.query.get(question_id),
        s3_key=key,
        user_agent=UserAgentSchema().dump(request.user_agent)[0]
        )
    db.session.add(v)
    db.session.commit()
    return VideoSchema().jsonify(v)
