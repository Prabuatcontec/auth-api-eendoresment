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
def modellist():
    user = Users.query.filter_by(username='brian.crehan@azmoves.com').first()
    responseBody = { "results": user.username }
    return jsonify(responseBody), status.HTTP_200_OK
