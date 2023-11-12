from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase

from settings import USER, DATABASE_PASSWORD, PORT, HOST, DATABASE_NAME


DB_URL = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(USER, DATABASE_PASSWORD, HOST, PORT, DATABASE_NAME)


class Base(DeclarativeBase):
    pass


engine = create_engine(DB_URL)

Base.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
