from time import sleep
from flask import Blueprint, request, Response, session, Flask, jsonify
from mysqlConnect import Connection
from flask_api import status


blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)

from authentication.models import Users 

@blueprint.route('/login')
def authentication():
    user = Users().encode_auth_token(123, 'brian.crehan@azmoves.com')
    responseBody = { "token": user }
    return jsonify(responseBody), status.HTTP_200_OK

@blueprint.route('/decode')
def decode_token():
    user = Users().encode_auth_token(123, 'brian.crehan@azmoves.com')
    user = Users().decode_auth_token(user)
    responseBody = { "results": user }
    return jsonify(responseBody), status.HTTP_200_OK
