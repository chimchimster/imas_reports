import sys
import logging


class DatabaseLogHandler(logging.Handler):

    _some_instance_value = None

    def __new__(cls, *args, **kwargs):
        cls.__setup()
        return super.__new__(cls)

    def __enter__(self):
        self.lock.acquire()
        self._send_log()
        self.lock.release()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.lock.locked():
            if exc_type:
                sys.stderr.write(f'Database Error: {exc_val}\nTraceback: {exc_tb}')
        else:
            self.lock.release()
            self.__exit__(exc_type, exc_val, exc_tb)

    @classmethod
    def __setup(cls):
        pass

    def __parse_log_format(self):
        pass

    def _send_log(self):
        self.__parse_log_format()


