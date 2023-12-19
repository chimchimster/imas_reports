import uuid
import json

from flask import request
from flask_restful import Resource
from kafka import load_kafka_settings, KafkaProducer
from logs.handlers import LokiLogger


class ReportQueue(Resource):

    @staticmethod
    def post() -> json:
        """ В ответ на метод POST создается задача
            и отправляется в брокер Kafka.
            Для задачи генерируется уникальный ключ,
            который возвращается пользователю для
            отслеживания состояния выполнения задачи. """

        request_json: request = request.get_json()
        json_string: json = json.dumps(request_json)
        json_bytes: bytes = json_string.encode('utf-8')

        task_unique_identifier: uuid = uuid.uuid4()
        settings_for_logger = json.loads(json_string)[-1]
        with LokiLogger(
                'Start handling report',
                report_id=str(task_unique_identifier),
                **settings_for_logger
        ):

            response_data: dict = {
                'user_unique_identifier': str(task_unique_identifier),
            }
            response_json: json = json.dumps(response_data)

            bs_serv, reports_topic, reports_ready_topic, sasl_username, sasl_password = load_kafka_settings()

            producer: KafkaProducer = KafkaProducer(
                bootstrap_server=bs_serv,
                topic=reports_topic,
                timeout=1000,
                sasl_username=sasl_username,
                sasl_password=sasl_password,
            )

            producer.send_message(
                key=str(task_unique_identifier),
                message=json_bytes,
            )

            producer.producer_poll()
            producer.producer_flush()

            return response_json, 200
