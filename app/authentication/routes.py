from time import sleep
from flask import Blueprint, request, Response, session, Flask, jsonify
from mysqlConnect import Connection
import os
import glob

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)

@blueprint.route('/login')
def modellist():
    responseBody = { "results": 1222 }
    return jsonify(responseBody), 200
