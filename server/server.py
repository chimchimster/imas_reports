import sys
import logging

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask.logging import default_handler


if __name__ == '__main__':

    root = logging.getLogger()
    root.addHandler(default_handler)

    app = Flask(__name__, static_folder='static')
    api = Api(app)
    CORS(app)

    from routes import api_routes
    for api_route, controller in api_routes:
        api.add_resource(controller, api_route)

    try:
        # from waitress import serve
        # serve(app, host='0.0.0.0', port=5000)
        app.run('0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        sys.exit(0)
