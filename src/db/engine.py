from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from settings import USER, DATABASE_PASSWORD, PORT, HOST, DATABASE_NAME


Base = declarative_base()
engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(USER, DATABASE_PASSWORD, HOST, PORT, DATABASE_NAME))

Base.metadata.create_all(engine)
