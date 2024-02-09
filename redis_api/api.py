import os
import redis


class ReportStorageRedisAPI:

    def __new__(cls, *args, **kwargs):

        cls._connection = redis.Redis(
            host=kwargs.get('host'),
            port=kwargs.get('port'),
            db=kwargs.get('db'),
            password=kwargs.get('password'),
            protocol=3,
        )

        return super().__new__(cls)

    @property
    def connection(self):
        return self._connection
