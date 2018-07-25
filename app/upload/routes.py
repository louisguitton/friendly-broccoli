from flask import current_app, jsonify, flash, request, render_template
from flask_login import login_required
import boto3
from botocore.exceptions import ParamValidationError

from app.upload import bp


s3_client = boto3.client('s3')


@bp.route('/url')
@login_required
def get_signed_url():
    # http://127.0.0.1:5000/upload/url?prefix=bar/baz&key=test.csv&content_type=text/csv
    prefix = request.args.get('prefix', default = None, type = str)
    key = request.args.get('key', default = None, type = str)
    content_type = request.args.get('content_type', default = None, type = str)

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
            'Bucket': current_app.config["S3"]["S3_BUCKET"],
            'Key': "{}/{}".format(prefix, key),
            'ContentType': content_type
            })

        return jsonify({"url": url})
    except ParamValidationError:
        return "need more args"


@bp.route('/', methods=['GET', 'POST'])
def upload():
    return render_template('upload/form.html')