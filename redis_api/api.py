import os
import redis


class ReportStorageRedisAPI:

    def __new__(cls, *args, **kwargs):

        cls._connection = redis.Redis(
            host=os.environ.get('REDIS_HOST'),
            port=os.environ.get('REDIS_PORT'),
            db=os.environ.get('REDIS_DB'),
            protocol=3,
        )

        return super().__new__(cls)

    @property
    def connection(self):
        return self._connection
