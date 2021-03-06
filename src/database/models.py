import datetime
from sqlalchemy import Boolean, Column, String, Integer, DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, BigInteger
from sqlalchemy.dialects.postgresql import MONEY

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    idx = Column(BigInteger, primary_key=True)
    email = Column(String)
    dateOfMailSend = Column(DateTime)
    dateOfaddingRoles = Column(DateTime)
    grade = Column(String)
    faculty = Column(String)

    def __repr__(self):
        return (
            "<User(idx='%d', email='%s', dateofregistration='%s', grade='%s', faculty='%s')>"
            % (self.idx, self.email, self.dateofregistration, self.grade, self.faculty)
        )


class registrationUser(Base):
    __tablename__ = "registrationUser"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    idofuser = Column(BigInteger)
    email = Column(String)
    dateOfMailSend = Column(DateTime)
    token = Column(String)
    nameofuser = Column(String)

    def __repr__(self):
        return (
            "<User(idx='%d', idofuser='%s',email='%s', date='%s', token='%s', faculty='%s')>"
            % (self.idx, self.idofuser, self.email, self.date, self.token)
        )
