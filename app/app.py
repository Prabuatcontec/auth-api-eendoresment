from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from mysqlConnect import Connection

# from api import api_blueprint

import os

load_dotenv()


MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_URL = os.getenv("MYSQL_URL")
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, DDD World!</p>"

@app.route("/health")
def health():
    return jsonify(status='up')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)