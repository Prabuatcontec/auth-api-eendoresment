from sys import api_version
from apispec import APISpec
from flask import Flask, jsonify, render_template, send_from_directory
from importlib import import_module
from flask_sqlalchemy import SQLAlchemy
from app.config import config_dict
from decouple import config
from dotenv import load_dotenv
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields

import os
load_dotenv()

db = SQLAlchemy()
 
app = Flask(__name__, template_folder='swagger/templates')
app.config['SECRET_KEY'] = config('SECRET_KEY', default=None)
app.config['JWT_PRIVATE_KEY'] = config('JWT_PRIVATE_KEY', default=None)
app.config['JWT_PUBLIC_KEY'] = config('JWT_PUBLIC_KEY', default=None)
app.config['JWT_PASE_PHRASE'] = config('JWT_PASE_PHRASE', default=None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

spec = APISpec(
title='flask-api-swagger-doc',
version='1.0.0',
openapi_version='3.0.2',
plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())



class TodoResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Boolean()


class TodoListResponseSchema(Schema):
    todo_list = fields.List(fields.Nested(TodoResponseSchema))


@app.route('/todo')
def todo():
    """Get List of Todo
    ---
    get:
        description: Get List of Todos
        responses:
            200:
                description: Return a todo list
                content:
                    application/json:
                        schema: TodoListResponseSchema
    """

    dummy_data = [{
        'id': 1,
        'title': 'Finish this task',
        'status': False
    }, {
        'id': 2,
        'title': 'Finish that task',
        'status': True
    }]

    return TodoListResponseSchema().dump({'todo_list': dummy_data})


with app.test_request_context():
    spec.path(view=todo)


@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', path)


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    for module_name in (['authentication']):
        module = import_module('app.{}.routes'.format(module_name))
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
