from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from routes import api_routes
from kafka_manager import KafkaManager
from kafka import load_kafka_settings

app = Flask(__name__, static_folder='static')
api = Api(app)
CORS(app)

for api_route, controller in api_routes:
    api.add_resource(controller, api_route)


if __name__ == '__main__':
    bootstrap_servers, reports_topic, reports_ready_topic = load_kafka_settings()

    with KafkaManager(
        bootstrap_servers=bootstrap_servers,
        reports_topic=reports_topic,
        reports_ready_topic=reports_ready_topic,
        producer_timeout=1000,
        consumer_timeout=1.0,
        group_id='none',
    ):
        app.run(host='0.0.0.0', debug=True)
else:
    print('Дружище, ты пойми, это не библиотека. Постарайся не импортировать файлы с точкой входа.')
