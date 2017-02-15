from flask import g
from flask_httpauth import HTTPTokenAuth

from werkzeug.exceptions import BadRequest

from models.user import User

auth = HTTPTokenAuth()


@auth.verify_token
def verify_password(token):
    """ verify user's password using auth tokens """

    user = User.verify_auth_token(token)
    if not user:
        raise BadRequest('Invalid Token')
    g.user = user
    return True
