import logging
import boto3, botocore


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
