### crud.py ###

from datetime import datetime

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from src.database.models import Base
from loguru import logger

import sys

sys.path.append("/app")
from settings import DATABASE_URL



def initTable():
    logger.info("database conncted succes")
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
