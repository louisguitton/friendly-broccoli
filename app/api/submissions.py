from flask import jsonify
from app.models import Submission, SubmissionSchema
from app.api import bp


@bp.route('/submissions')
def list_submissions():
    all_submissions = Submission.query.all()
    result = SubmissionSchema(many=True).dump(all_submissions)
    return jsonify(result.data)

@bp.route('/submissions/<id>')
def submission_detail(id):
    submission = Submission.query.get(id)
    return jsonify(submission.to_dict())
