import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from billing.billing_sqla import create_application, SqlaBilling
from billing.models import Base, Application, Hits, Times


TEST_DATABASE_URI = "sqlite:///test_database.db"


class Test3Scale:
    def __init__(self):
        pass

    def setUp(self):
        # Create a test database
        self.test_database_uri = TEST_DATABASE_URI

        # Create the sqlalchemy engine and the db itself.
        self.engine = create_engine(self.test_database_uri)
        Base.metadata.create_all(self.engine)
        self.smaker = sessionmaker(self.engine)

    def tearDown(self):
        # Destroy the database.
        os.remove("test_database.db")

    def test_database_creation(self):
        # If the tables don't exist exceptions will be raised.
        self.engine.execute("SELECT 1 FROM Application")
        self.engine.execute("SELECT 1 FROM Hits")
        self.engine.execute("SELECT 1 FROM Times")

    def test_application_creation(self):
        id = create_application(self.test_database_uri, "Test App", "Test App Description")
        assert id is not None

        db = self.smaker()
        app = db.query(Application).filter_by(id=id).first()
        assert app is not None
        assert type(app) == Application
        assert app.name == "Test App"
        assert app.description == "Test App Description"


    def test_report_hits(self):
        # Create a test application and report hits.
        appid = create_application(self.test_database_uri, "Test App", "Test App Description")
        api = SqlaBilling(self.test_database_uri, appid)
        api.report_hits(15)

        # Verify that all is correct.
        db = self.smaker()
        hits = db.query(Hits).filter_by(app_id=appid).all()
        assert hits is not None
        assert len(hits) == 1
        assert hits[0].hits == 15

    def test_report_time(self):
        # Create a test application and report times..
        appid = create_application(self.test_database_uri, "Test App", "Test App Description")
        api = SqlaBilling(self.test_database_uri, appid)
        api.report_time(60)

        # Verify that all is correct.
        db = self.smaker()
        times = db.query(Times).filter_by(app_id=appid).all()
        assert times is not None
        assert len(times) == 1
        assert times[0].time == 60