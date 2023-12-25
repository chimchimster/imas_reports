
import sqlalchemy.exc

from sqlalchemy import insert, update

from modules.database.models import Base
from modules.database.engine import engine
from modules.database.session import LocalSession
from modules.logs.decorators import tricky_loggy
from modules.logs.handlers import LokiLogger
from modules.database.models.storage import ReportMetaStorage


class ReportStorageMySQLAPI:

    _report_id = None

    def __new__(cls, *args, **kwargs):

        with LokiLogger(None):
            try:
                Base.metadata.create_all(bind=engine)
            except sqlalchemy.exc.IntegrityError:
                pass

        return super().__new__(cls)

    def __init__(self, task_uuid: str, user_id: int):
        self._task_uuid = task_uuid
        self._user_id = user_id

    @tricky_loggy
    def on_startup(self):

        insert_stmt = insert(ReportMetaStorage).values(
            user_id=self._user_id,
            report_key=self._task_uuid
        ).returning(ReportMetaStorage.report_id)

        try:
            with LocalSession() as session:
                stmt_result = session.execute(insert_stmt)
                report_id = stmt_result.scalar()
                session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e

        if report_id is not None:
            self._report_id = report_id

    @tricky_loggy
    def on_shutdown(self, status: str):

        if self._report_id is None:
            return

        update_stmt = update(ReportMetaStorage).values(
            status=status
        ).filter(
            ReportMetaStorage.report_id == self._report_id
        )

        try:
            with LocalSession() as session:
                session.execute(update_stmt)
                session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e

