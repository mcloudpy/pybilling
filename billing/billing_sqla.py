from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Hits, Times, User


class SqlaBilling(object):
    def __init__(self, uid):
        self._uid = uid
        self._engine = create_engine('sqlite:///database.db')
        Base.metadata.bind = self._engine
        DBSession = sessionmaker(bind=self._engine)
        self._session = DBSession()

    def report_hits(self, hits):
        new_hits = Hits(hits=hits, user_id=self._uid)
        self._session.add(new_hits)
        self._session.commit()

    def report_time(self, time):
        new_time = Times(time=time, user_id=self._uid)
        self._session.add(new_time)
        self._session.commit()