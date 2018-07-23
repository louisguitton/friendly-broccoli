from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes_auth0, auth0_management_api