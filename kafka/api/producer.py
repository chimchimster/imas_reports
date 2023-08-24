import sys

from confluent_kafka import Producer, KafkaError


class KafkaProducer:
    def __init__(
            self,
            bootstrap_server: str,
            topic: str,
            timeout: int,
    ) -> None:
        self._bootstrap_server = bootstrap_server
        self._topic = topic
        self._timeout = timeout
        self._producer = self.__configure_producer()

    def __configure_producer(self) -> Producer:

        conf = {
            'bootstrap.servers': self.bootstrap_server,
        }

        prdcr: Producer = Producer(conf)

        return prdcr

    @property
    def bootstrap_server(self) -> str:
        return self._bootstrap_server

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def producer(self) -> Producer:
        return self._producer

    @property
    def timeout(self) -> float:
        return self._timeout

    def producer_poll(self) -> None:
        self.producer.poll(self.timeout)

    def producer_flush(self) -> None:
        self.producer.flush()

    def send_message(self, key: str, message: bytes) -> None:
        """ Метод кладет в очередь задач сообщение
        с уникальным идентификатором по которому определяется партиция."""

        def on_delivery(error: KafkaError, msg: str) -> None:
            """ Колбэк - доставлено ли сообщение. """

            if error is not None:
                sys.stderr.write(f'Отправка сообщения не удалась.\n Ошибка:\n{error}')
            else:
                sys.stdout.write(f'Удачная отправка сообщения в партицию {msg.partition()} топика {msg.topic()}\n\n')

        try:
            self.producer.produce(
                topic=self.topic,
                key=key,
                value=message,
                callback=on_delivery,
            )
        except KafkaError.FailedPayloads as e:
            print(e)
        except KafkaError.KafkaTimeout as e:
            print(e)
        except KafkaError.ConnectionError as e:
            print(e)
        except KafkaError.SerializationError as e:
            print(e)
        except KafkaError as e:
            print(e)