from time import sleep
from flask import Blueprint, request, Response, session, Flask, jsonify, abort
from sqlalchemy import false
from mysqlConnect import Connection
from flask_api import status
import bcrypt

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)

from authentication.models import Users 

@blueprint.route('/credential')
def auth():
    username = "prabum1985@gmail.com"
    passwd = b'Eendor@123'

    # hashed = b'59ffcf24ec564c07795bd11918ee6cb91d9f67077d505f021ee96dc45b97dd2d1d50554e3639d3664ae68ed277d0c8a4bf7c'
    # hashed = bcrypt.hashpw(passwd, salt)
    # print("hash")
    # print(hashed)
 
    hashed = b'$2y$13$Keux2pQHAwiuVeerXQGBcuuk.ea9C9K0jl6xhlkMFRUenyVnrAeu.'
    
    if bcrypt.checkpw(passwd, hashed):
        return "match"
    else:
        return "does not match"
        
@blueprint.route('/login', methods = ['POST'])
def authentication():
    username = request.form['_username'] 
    password = request.form['_password']
    validation = False
    if username is None or password is None:
        validation = True
    user = Users.query.filter_by(username = username).first()
    if user is None:
        validation = True
    if validation == False:
        token = Users().encode_auth_token(user.id, user.username, user.password, password)
        if token == False:
            validation = True
        else: 
            return jsonify({ "token": token }), status.HTTP_200_OK
    if validation == True:
        return jsonify({ "code": status.HTTP_400_BAD_REQUEST, "message": "Bad credentials" }), status.HTTP_400_BAD_REQUEST
    

@blueprint.route('/decode')
def decode_token():
    user = Users().encode_auth_token(123, 'brian.crehan@azmoves.com')
    user = Users().decode_auth_token(user)
    responseBody = { "results": user }
    return jsonify(responseBody), status.HTTP_200_OK
