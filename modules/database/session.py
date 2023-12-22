from sqlalchemy.orm import sessionmaker, Session

from modules.database.engine import engine as eng


LocalSession = sessionmaker(eng, class_=Session, expire_on_commit=True)
