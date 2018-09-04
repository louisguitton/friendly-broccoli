from flask import render_template, current_app
from flask_wtf.csrf import CSRFError

from app import db
from app.errors import bp


# Error handlers.
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    current_app.logger.error('Server Error: %s', (error))
    return render_template('errors/500.html'), 500


@bp.app_errorhandler(Exception)
def unhandled_exception(e):
    db.session.rollback()
    current_app.logger.error('Unhandled Exception: %s', (e))
    return render_template('errors/500.html'), 500


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403


@bp.errorhandler(CSRFError)
def csrf_error(e):
    return render_template('errors/csrf_error.html', reason=e.description), 400
