from flask import render_template, request, flash, redirect, url_for
from logging import Formatter, FileHandler
import logging

from app import app
from forms import ApplyForm, LoginForm, RegisterForm, ForgotForm
import config


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html', config=config)

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplyForm()
    # if form.validate_on_submit():
    if request.method == 'POST' and form.validate():
        msg = 'Submission requested for user {}, mail={}'.format(
            form.name.data, form.email.data)
        app.logger.info(msg)
        flash(msg)
        return redirect(url_for('home'))
    return render_template('forms/apply.html', global_data=config.global_data, form=form)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
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
