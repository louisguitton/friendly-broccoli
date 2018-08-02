from flask import jsonify
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from linkedin import linkedin

from config import Config
from app.auth import bp


def get_management_api_client():
    get_token = GetToken(Config.AUTH0_DOMAIN)
    token = get_token.client_credentials(
        Config.AUTH0_NON_INTERACTIVE_CLIENT_ID,
        Config.AUTH0_NON_INTERACTIVE_CLIENT_SECRET, 
        Config.AUTH0_BASE_URL + '/api/v2/'
        )
    mgmt_api_token = token['access_token']

    auth0 = Auth0(Config.AUTH0_DOMAIN, mgmt_api_token)
    return auth0

def get_user(user_id):
    auth0 = get_management_api_client()
    return auth0.users.get(user_id)

@bp.route('/api/users/<user_id>')
def users(user_id):
    return jsonify(get_user(user_id))

def get_from_linkedin_api(access_token_str):
    application = linkedin.LinkedInApplication(token=access_token_str)    

    #Get own Profile 
    my_profile = application.get_profile(selectors=[
        'id', 
        'first-name',
        'last-name', 
        'location', 
        'industry',
        'num-connections', 
        'summary'
        ])
    print(my_profile)