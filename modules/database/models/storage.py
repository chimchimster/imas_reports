import enum
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, Enum, Index

from modules.database.models.base import Base


class ReportMetaStorage(Base):

    __tablename__ = 'report_meta_storage'

    __table_args__ = (
        Index('report_key_idx', 'report_key'),
    )

    class ReportStatus(enum.Enum):
        in_progress = 'in_progress'
        ready = 'ready'
        error = 'error'

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    report_key = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    status = Column(Enum(ReportStatus), default=ReportStatus.in_progress)
