from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from routes import api_routes
from kafka_manager import KafkaManager
from kafka import load_kafka_settings
from logs.handlers import LokiLogger

app = Flask(__name__, static_folder='static')
api = Api(app)
CORS(app)

for api_route, controller in api_routes:
    api.add_resource(controller, api_route)


if __name__ == '__main__':
    bootstrap_server, reports_topic, reports_ready_topic, sasl_username, sasl_password = load_kafka_settings()

    with KafkaManager(
        bootstrap_server=bootstrap_server,
        reports_topic=reports_topic,
        reports_ready_topic=reports_ready_topic,
        producer_timeout=1000,
        consumer_timeout=1.0,
        group_id='none',
        sasl_username=sasl_username,
        sasl_password=sasl_password
    ) as manager:
        with LokiLogger('Start app'):
            app.run(host='0.0.0.0', debug=True)

