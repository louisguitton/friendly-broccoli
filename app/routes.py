import time
from flask import render_template, request, flash, redirect, url_for, send_from_directory
from logging import Formatter, FileHandler
import logging
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime

from app.models import User
from app import app
from app.forms import ApplyForm, LoginForm, RegistrationForm, ForgotForm
from app import db
import config
from app.helpers import upload_file_to_s3


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
def index():
    return render_template('pages/placeholder.home.html', config=config)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') # url_for ?
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('forms/login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('forms/register.html', title='Register', form=form)

@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    if current_user.username == username:
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('pages/user.html', user=user)
    else:
        flash("Sorry, you can see only your profile.")
        return redirect(url_for('index'))

@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplyForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.linkedin_handle = form.linkedin_handle.data 
        db.session.commit()
        msg = 'Thanks, submission requested for user {}, mail={}'.format(
            form.name.data, current_user.email)
        flash(msg)
        return redirect(url_for('find_question'))
    # TODO: enlever l'usage de config.global_data
    return render_template('forms/apply.html', global_data=config.global_data, form=form)


@app.route('/questions', methods=['GET', 'POST'])
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
            output   	  = upload_file_to_s3(video, app.config["S3_BUCKET"])
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
        return render_template('forms/video.html', global_data=config.global_data, video_settings=video_settings)     



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
