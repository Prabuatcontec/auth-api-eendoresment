from flask import Flask, jsonify
from importlib import import_module

from flask_sqlalchemy import SQLAlchemy
from config import config_dict
from decouple import config
from dotenv import load_dotenv

 
import os
load_dotenv()


db = SQLAlchemy()
 
app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY', default=None)
app.config['JWT_PRIVATE_KEY'] = config('JWT_PRIVATE_KEY', default=None)
app.config['JWT_PUBLIC_KEY'] = config('JWT_PUBLIC_KEY', default=None)
app.config['JWT_PASE_PHRASE'] = config('JWT_PASE_PHRASE', default=None)

def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    for module_name in (['authentication']):
        module = import_module('{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
        db.session.close()

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

 
# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

app_config = config_dict[get_config_mode.capitalize()]

app.config.from_object(app_config)
register_extensions(app)
register_blueprints(app)    
configure_database(app)

@app.route("/")
def hello_world():
    return "<p>Hello, DDD World!</p>"

@app.route("/health")
def health():
    return jsonify(status='up')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)