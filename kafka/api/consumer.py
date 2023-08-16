from confluent_kafka import Consumer, TopicPartition, KafkaError


class KafkaConsumer:
    def __init__(
            self,
            bootstrap_servers: str,
            topic: str,
            timeout: float,
            group_id: str,
            enable_auto_commit: bool = False,
            auto_offset_reset: str = 'earliest',
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._timeout = timeout
        self._group_id = group_id
        self._enable_auto_commit = enable_auto_commit
        self._auto_offset_reset = auto_offset_reset

        self._consumer: Consumer = self.__configure_consumer()

    def __configure_consumer(self) -> Consumer:

        conf = {
            'bootstrap.servers': self._bootstrap_servers,
            'group.id': self._group_id,
            'enable.auto.commit': self._enable_auto_commit,
            'auto.offset.reset': self._auto_offset_reset,
        }

        cnsmr: Consumer = Consumer(conf)

        return cnsmr

    @property
    def consumer(self) -> Consumer:
        return self._consumer

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def timeout(self) -> float:
        return self._timeout

    def __assign_consumer_to_topic_and_partition(self):
        self.consumer.assign([TopicPartition(self.topic, 0),])

    def retrieve_message(self):

        self.__assign_consumer_to_topic_and_partition()

        while True:
            msg = self.consumer.poll(self.timeout)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error().str()}")
                    break
            print(f"Key: {msg.key()} received message: {msg.value().decode('utf-8')} from partition {msg.partition()}")