from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, request, send_from_directory
from flask_login import current_user, login_required

from app import db
from app.main.forms import ApplyForm
from app.models import Question, Submission
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/robots.txt')
@bp.route('/sitemap.xml')
def static_from_root():
    return send_from_directory('static', request.path[1:])

@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/interview', methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplyForm(obj=current_user, meta={'csrf': False})
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.linkedin_url = form.linkedin_url.data

        s = Submission(applicant=current_user._get_current_object())

        db.session.add(s)
        db.session.commit()

        session['submission'] = s.to_dict()

        msg = 'Thanks, submission requested for user {}, mail={}'.format(
            form.name.data, current_user.email)
        flash(msg)
        return redirect(url_for('main.find_question'))

    questions = Question.query.order_by("order_pos asc").all()
    return render_template('apply.html', questions=questions, form=form)


@bp.route('/questions')
def find_question():
    if session.get('submission') is not None:
        video_settings = {
            'controls': True,
            'fluid': True,
            'plugins': {
                'record': {
                    'audio': True,
                    'video': True,
                    'debug': False
                }
            }
        }
        questions = Question.query.order_by("order_pos asc").all()
        return render_template('video.html', questions=questions, video_settings=video_settings)
    return redirect(url_for('main.apply'))


@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@bp.route('/impressum')
def impressum():
    return render_template('impressum.html')
