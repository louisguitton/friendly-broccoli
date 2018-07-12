from functools import wraps
import json
from six.moves.urllib.parse import urlencode

from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db, oauth, Config
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


auth0 = oauth.register(
    'auth0',
    client_id=Config.AUTH0_CLIENT_ID,
    client_secret=Config.AUTH0_CLIENT_SECRET,
    api_base_url=Config.AUTH0_BASE_URL,
    access_token_url=Config.AUTH0_BASE_URL + '/oauth/token',
    authorize_url=Config.AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@bp.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri=Config.AUTH0_CALLBACK_URL, 
        # audience=Config.AUTH0_AUDIENCE
        audience=Config.AUTH0_BASE_URL + '/api/v2/'
    )

@bp.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    resp2 = auth0.get('users', params={'id': userinfo['sub']})
    print(resp2)
    # userinfo2 = resp2.json()
    # session['jwt_payload'] = resp2
    
    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    user = {
        'user_id': userinfo['sub'],
        "name": userinfo['name'],
        "username": userinfo['nickname'],
        "avatar": userinfo['picture'],
        "email": userinfo['email']
        # "location":
        # "linkedin_handle"
        # "password_hash"
        # "last_seen"
    }
    session['user'] = user
    return redirect(url_for('auth.dashboard'))


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'user' not in session:
      # Redirect to Login page here
      flash('You must log in for that.')
      return redirect(url_for('main.index'))
    return f(*args, **kwargs)

  return decorated

@bp.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('auth/dashboard.html',
                           user=session['user'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@bp.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('main.index', _external=True), 'client_id': Config.AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
