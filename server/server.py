from .setup import api, app
from .routes import api_routes, socket_routes
from flask_socketio import SocketIO

socketio = SocketIO(
    app,
    async_mode='gevent',
    cors_allowed_origins='*',
)

for api_route, controller in api_routes:
    api.add_resource(controller, api_route)

for socket_route, namespace in socket_routes:
    socketio.on_namespace(namespace(socket_route))
