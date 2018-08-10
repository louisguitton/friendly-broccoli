import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_principal import Principal
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from authlib.flask.client import OAuth
from flask_admin import Admin
from flask_marshmallow import Marshmallow
from flask_wtf import CSRFProtect
from config import Config
from app.admin import CustomIndexView
from celery import Celery
import celeryconfig

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ''
bootstrap = Bootstrap()
oauth = OAuth()
moment = Moment()
principals = Principal()
celery = Celery(__name__, broker=Config.BROKER_URL)
ma = Marshmallow()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    oauth.init_app(app)
    moment.init_app(app)
    admin = Admin(
        app, 
        name='videocollect', 
        template_mode='bootstrap3', 
        index_view=CustomIndexView(), 
        base_template='admin/main.html'
    )
    principals.init_app(app)
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    ma.init_app(app)
    csrf.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import init_admin, register_principal_identity_signal
    init_admin(admin)
    register_principal_identity_signal(app)

    from app.upload import bp as upload_bp
    app.register_blueprint(upload_bp, url_prefix='/upload')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('PersonalityInterview startup')

    return app


from app import models