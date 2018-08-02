import logging
import boto3
from flask import request, flash, redirect, current_app
from werkzeug.utils import secure_filename


def upload_file_to_s3(file, s3_config, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=s3_config["S3_KEY"],
        aws_secret_access_key=s3_config["S3_SECRET"]
    )

    try:
        s3.upload_fileobj(
            file,
            s3_config["S3_BUCKET"],
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        logging.error("Something Happened: {}".format(e))
        return e

    return "{}{}".format(s3_config["S3_LOCATION"], file.filename)


def post_video_to_S3():
    # upload(request, question_id)
    if 'file' not in request.files:
        flash('No file key in request.files')
        return redirect(request.url)
    video = request.files['file']
    """
    These attributes are also available

    video.filename               # The actual name of the file
    video.content_type
    video.content_length
    video.mimetype

    """

    # if user does not select file, browser also
    # submit an empty part without filename
    if video.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if video and allowed_file(video.filename):
        video.filename = secure_filename(video.filename)
        output = upload_file_to_s3(video, current_app.config["S3"])
        return output
    return redirect(request.url)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
