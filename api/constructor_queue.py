import time
import uuid
import json
from flask import request
from flask_restful import Resource
from confluent_kafka import Producer, Consumer, KafkaError
from kafka import load_kafka_settings, KafkaProducer, KafkaConsumer


class DocxReportQueue(Resource):
    def post(self) -> json:
        """ В ответ на метод POST создается задача
            и отправляется в очередь Kafka.
            Для задачи генерируется уникальный ключ,
            который возвращается пользователю для
            отслеживания состояния выполнения задачи. """

        request_json: request = request.get_json()
        json_string: json = json.dumps(request_json)
        json_bytes: bytes = json_string.encode('utf-8')

        task_unique_identifier: uuid = uuid.uuid4()

        response_data: dict = {
            'user_unique_identifier': str(task_unique_identifier),
        }

        response_json: json = json.dumps(response_data)

        bs_serv, topic = load_kafka_settings()

        producer: KafkaProducer = KafkaProducer(
            bootstrap_servers=bs_serv,
            topic=topic,
            timeout=1000,
        )

        producer.send_message(
            key=str(task_unique_identifier),
            message=json_bytes,
        )

        producer.producer_poll()
        producer.producer_flush()

        consumer: KafkaConsumer = KafkaConsumer(
            bootstrap_servers=bs_serv,
            topic=topic,
            timeout=1.0,
            group_id='my_group',

        )

        consumer.retrieve_message()

        return response_json, 200
