import json
import os
from typing import Any

from utils import RemoveDirsMixin
from flask import send_from_directory
from tools import WordCreator, PDFCreator
from kafka import load_kafka_settings, KafkaConsumer


class QueueConsumer(KafkaConsumer, RemoveDirsMixin):

    def consume(self):
        while True:
            key, value = next(self.retrieve_message())
            self.process_task(key, value)

    def process_task(self, key: bytes, value: str) -> Any:
        query = json.loads(value)

        task_uuid = key.decode('utf-8')

        report = WordCreator(query, task_uuid)

        report.render_report()

        _uuid = key

        response = send_from_directory(
            os.path.join(
                os.getcwd(),
                'word',
                'merged',
                _uuid,
            ),
            'merged_output.docx',
        )

        dirs_to_delete = [
            os.path.join(
                os.getcwd(),
                'word',
                'merged',
            ),
            os.path.join(
                os.getcwd(),
                'word',
                'temp',
            ),
            os.path.join(
                os.getcwd(),
                'word',
                'temp_templates',
            ),
        ]

        for _dir in dirs_to_delete:
            self.remove_dir(_dir, _uuid)

        self.remove_temp_tables_dirs(_uuid)

        return response