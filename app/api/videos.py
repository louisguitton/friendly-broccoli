from flask import jsonify
from app.models import Video, VideoSchema
from app.api import bp


@bp.route('/videos')
def list_videos():
    all_videos = Video.query.all()
    result = VideoSchema(many=True).dump(all_videos)
    return jsonify(result.data)

@bp.route('/videos/<id>')
def video_detail(id):
    video = Video.query.get(id)
    return jsonify(video.to_dict())
