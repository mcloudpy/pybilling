
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Hits(Base):
    __tablename__ = 'hits'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    hits = Column(Integer)

class Times(Base):
    __tablename__ = 'times'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    time = Column(Integer)

if __name__ == "__main__":

    # Create the engine (simple sqlalchemy db for now)
    # TODO: Make this customizable etc etc.
    engine = create_engine('sqlite:///database.db')

    # Create all tables.
    Base.metadata.create_all(engine)