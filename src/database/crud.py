### crud.py ###

from datetime import datetime

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from src.database.models import Base
from loguru import logger

import sys, os

sys.path.append("../")
print(sys.path)
print(os.listdir('/app'))
from settings import DATABASE_URL


def initTable():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    logger.info("database conncted succes")
    return session
