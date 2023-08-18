from queue import Queue
from flask import Flask
from flask_cors import CORS
from threading import Thread
from flask_restful import Api
from routes import api_routes
from consumers import QueueConsumer
from kafka import load_kafka_settings

app = Flask(__name__, static_folder='static')
api = Api(app)
CORS(app)

for api_route, controller in api_routes:
    api.add_resource(controller, api_route)


if __name__ == '__main__':
    _bs_serv, _topic = load_kafka_settings()

    tasks_queue = Queue()
    with QueueConsumer(
        bootstrap_servers=_bs_serv,
        topic=_topic,
        timeout=1.0,
        group_id='none',
        queue=tasks_queue,
    ) as consumer:
        kafka_consumer_thread = Thread(target=consumer.consume)
        kafka_consumer_thread.start()
        app.run(host='0.0.0.0', debug=True)
else:
    print('Дружище, ты пойми, это не библиотека. Постарайся не импортировать файлы с точкой входа.')
