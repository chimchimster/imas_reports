import sys
import logging
from flask_socketio import SocketIO

from setup import api, app


if __name__ == '__main__':

    root = logging.getLogger('waitress')
    root.setLevel(logging.INFO)

    from routes import api_routes, socket_routes

    for api_route, controller in api_routes:
        api.add_resource(controller, api_route)

    socketio = SocketIO(app, cors_allowed_origins="*")

    for socket_route, namespace in socket_routes:
        socketio.on_namespace(namespace(socket_route))

    try:
        # from waitress import serve
        # from paste.translogger import TransLogger
        # serve(TransLogger(socket_app, setup_console_handler=True), host='0.0.0.0', port=5010)

        socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True, port=5007)
    except KeyboardInterrupt:
        sys.exit(0)
