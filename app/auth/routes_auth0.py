from functools import wraps
import json
from six.moves.urllib.parse import urlencode
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session, current_app, g
from werkzeug.urls import url_parse
from werkzeug.local import LocalProxy
from flask_login import login_user, logout_user, current_user, login_required
from flask_principal import identity_changed, Identity, AnonymousIdentity
from app import db, oauth, Config
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app.auth.auth0_management_api import get_user


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
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    next_page = request.args.get('next')
    session['next'] = next_page

    return auth0.authorize_redirect(
        redirect_uri=Config.AUTH0_CALLBACK_URL, 
        audience=Config.AUTH0_AUDIENCE
    )

def register(user_json):
    user = User(
        auth0_id=user_json['user_id'],
        created_at=datetime.strptime(user_json['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        name=user_json['name'],
        nickname=user_json['nickname'], 
        email=user_json['email'],
        linkedin_url=user_json['publicProfileUrl'],
        last_login=datetime.strptime(user_json['last_login'], '%Y-%m-%dT%H:%M:%S.%fZ'),
    )
    for col in ['picture', 'headline', 'industry', 'summary']:
        if col in user_json:
            setattr(user, col, user_json[col])
    if 'location' in user_json:
        user.location = user_json['location']['name']
    
    flash('Congratulations, you are now a registered user!')
    return user


@bp.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    
    # Store the user information in flask session.
    session['jwt_payload'] = userinfo

    # Get a complete user profile and store it in flask session.
    user_id = userinfo['sub']
    user_full_profile = get_user(user_id)

    # Store user info in DB
    # Every time a users logs in, search the table for that user.
    user = User.query.filter_by(auth0_id=user_id).first()
    # If the user does not exist, create a new record.
    if user is None:
        user = register(user_full_profile)
    # If they do exist, update all fields, essentially keeping a local copy of all user data.
    else:
        user.auth0_id=user_full_profile['user_id']
        user.created_at=datetime.strptime(user_full_profile['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        user.name=user_full_profile['name']
        user.nickname=user_full_profile['nickname']
        user.email=user_full_profile['email']
        user.linkedin_url=user_full_profile['publicProfileUrl']
        user.last_login=datetime.strptime(user_full_profile['last_login'], '%Y-%m-%dT%H:%M:%S.%fZ')

        for col in ['picture', 'headline', 'industry', 'summary']:
            if col in user_full_profile:
                setattr(user, col, user_full_profile[col])
        if 'location' in user_full_profile:
            user.location = user_full_profile['location']['name']

    db.session.add(user)
    db.session.commit()

    login_user(user)

    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.email))
    
    next_page = None
    if 'next' in session:
        next_page = session.pop('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('auth.dashboard')
    return redirect(next_page)


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'auth/dashboard.html',
        user=current_user
    )

@bp.route('/logout')
def logout():
    # Clear session stored data
    logout_user()
    session.clear()

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    # Redirect user to logout endpoint
    params = {'returnTo': url_for('main.index', _external=True), 'client_id': Config.AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
