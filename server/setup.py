from flask import Flask
from flask_cors import CORS
from flask_restful import Api


def get_app():
    _app = Flask(__name__, static_folder='static')
    _api = Api(_app)
    CORS(_app, cors_allowed_origins='*')

    return _api, _app


api, app = get_app()
