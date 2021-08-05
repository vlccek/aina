### crud.py ###

from datetime import datetime

from sqlalchemy import create_engine
from ...settings import DATABASE_URI
from models import registrationUser, User, Base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import yaml


def initTable():
    print("connected")
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session
