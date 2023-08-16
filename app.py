from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from routes import api_routes
from confluent_kafka import Producer, Consumer, KafkaError

from kafka import load_kafka_settings, KafkaProducer


app = Flask(__name__, static_folder='static')
api = Api(app)
CORS(app)

for api_route, controller in api_routes:
    api.add_resource(controller, api_route)


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
else:
    print('Дружище, ты пойми, это не библиотека. Постарайся не импортировать файлы с точкой входа.')
