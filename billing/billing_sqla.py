from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Hits, Times, Application


def create_application(database_uri, name, description):
    """
    Creates a new Application and returns the id for the new application, which is what is needed
    to report usage for it.

    @param database_uri: URI of the database to use.
    @param name: Name of the new application.
    @param description: Description of the new application.

    @return: ID assigned to the new application, which is used for reporting usage.
    """
    engine = create_engine(database_uri)
    DBSession = sessionmaker(engine)
    session = DBSession()

    app = Application(name=name, description=description)
    session.add(app)
    session.commit()

    return app.id


class SqlaBilling(object):
    def __init__(self, database_uri, uid):
        self._uid = uid
        self._engine = create_engine(database_uri)
        Base.metadata.bind = self._engine
        DBSession = sessionmaker(bind=self._engine)
        self._session = DBSession()

    def report_hits(self, hits):
        new_hits = Hits(hits=hits, app_id=self._uid)
        self._session.add(new_hits)
        self._session.commit()

    def report_time(self, time):
        new_time = Times(time=time, app_id=self._uid)
        self._session.add(new_time)
        self._session.commit()