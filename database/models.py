from sqlalchemy import Column, Integer, String, Text, Date, DateTime,  BLOB, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    services = relationship("Service", backref="category")


class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(ForeignKey("category.id"))

    appointments = relationship("Appointment", backref="service")


class LastWork(Base):
    __tablename__ = "last_work"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.date.today())
    image = Column(BLOB)


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String(255), nullable=False)
    username = Column(String(255))
    client = Column(String(255))
    service_id = Column(ForeignKey("service.id"))
    time = Column(DateTime, nullable=False, unique=True)



def create_tables(engine):
    Base.metadata.create_all(engine, checkfirst=True)



    