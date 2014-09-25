
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class Application(Base):
    __tablename__ = 'application'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500), nullable=False)

class Hits(Base):
    __tablename__ = 'hits'
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey('application.id'))
    hits = Column(Integer)
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    app = relationship(Application)

class Times(Base):
    __tablename__ = 'times'
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey('application.id'))
    time = Column(Integer)
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    app = relationship(Application)

if __name__ == "__main__":

    # Create the engine (simple sqlalchemy db for now)
    # TODO: Make this customizable etc etc.
    engine = create_engine('sqlite:///database.db')

    # Create all tables.
    Base.metadata.create_all(engine)