import sys
import time
import uuid
import json
from flask import request
from flask_restful import Resource
from confluent_kafka import Producer, Consumer, KafkaError


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

        conf = {
            'bootstrap.servers': 'someserverip',
        }

        producer: Producer = Producer(conf)

        producer.produce('reports', key=str(task_unique_identifier), value=json_bytes)
        producer.poll(10000)
        producer.flush()

        conf = {
            'bootstrap.servers': 'someserverip',
            'group.id': "foo",
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest',
        }

        consumer: Consumer = Consumer(conf)
        consumer.subscribe(['reports'])
        start = time.time()
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
            else:
                print('%% %s [%d] at offset %d with key %s:\n' %
                      (msg.topic(), msg.partition(), msg.offset(),
                       str(msg.key())))
                print(msg.value())
                end = time.time()
                print(end - start)

        return response_json, 200
