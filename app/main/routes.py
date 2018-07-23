from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, send_from_directory, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.main.forms import ApplyForm
from app.models import User
from app.helpers import upload_file_to_s3
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplyForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.linkedin_url = form.linkedin_url.data 
        db.session.commit()
        msg = 'Thanks, submission requested for user {}, mail={}'.format(
            form.name.data, current_user.email)
        flash(msg)
        return redirect(url_for('main.find_question'))
    # TODO: enlever l'usage de config.global_data
    return render_template('apply.html', global_data=current_app.config["GLOBAL_DATA"], form=form)


@bp.route('/questions', methods=['GET', 'POST'])
def find_question():
    if request.method == "POST":
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
        else:
            return redirect(request.url)
    else:
        # TODO: enlever l'usage de config.global_data
        video_settings = {
                'controls': True,
                'width': 520,
                'height': 240,
                'fluid': False,
                'plugins': {
                    'record': {
                        'audio': True,
                        'video': True,
                        'maxLength': 30,
                        'debug': True
                    }
                }
            }
        return render_template('video.html', global_data=current_app.config["GLOBAL_DATA"], video_settings=video_settings)     



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
