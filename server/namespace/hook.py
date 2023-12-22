from flask_socketio import Namespace, emit


class SocketWebHookNamespace(Namespace):

    def on_connect(self):
        print(f"Присоеденился клиент")

    def on_disconnect(self):
        print(f"Клиент отключился")

    def on_message(self, msg):
        print(f"Клиент прислал сообщение: {msg}")
        emit('message', msg)
