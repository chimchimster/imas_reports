import sys
import logging

from flask import Flask
from flask_cors import CORS
from flask_restful import Api


if __name__ == '__main__':

    root = logging.getLogger('waitress')
    root.setLevel(logging.INFO)

    app = Flask(__name__, static_folder='static')
    api = Api(app)
    CORS(app)

    from routes import api_routes
    for api_route, controller in api_routes:
        api.add_resource(controller, api_route)

    try:
        from waitress import serve
        from paste.translogger import TransLogger

        serve(TransLogger(app, setup_console_handler=True), host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        sys.exit(0)
