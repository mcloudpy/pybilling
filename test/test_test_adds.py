import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from billing.models import Base, Hits, Application
from billingweb import flask_app as app
from billingweb import sqla


class TestTestAdds:
    def __init__(self):
        self.flask_app = None

    def setUp(self):
        # Redirect SQLA to the test database.
        sqla._db_eng = create_engine("sqlite:///test_database.db")
        Base.metadata.create_all(sqla._db_eng)
        sqla.db = sessionmaker(sqla._db_eng)

        # Flask too.
        app.config["DATABASE_URI"] = "sqlite:///test_database.db"

        self.flask_app = app.test_client()

    def tearDown(self):
        try:
            os.remove("test_database.db")
        except:
            pass

    def test_nothing(self):
        pass

    def test_index(self):
        """
        Check that the Index works.
        """
        ret = self.flask_app.get("/")
        assert ret.status_code == 200 or ret.status_code == 302

    def test_injected_test_database(self):
        # If the tables don't exist exceptions will be raised.
        sqla._db_eng.execute("SELECT 1 FROM Application")
        sqla._db_eng.execute("SELECT 1 FROM Hits")
        sqla._db_eng.execute("SELECT 1 FROM Times")
        sqla._db_eng.execute("INSERT INTO hits VALUES (5, 5, 5, 5)")

    def test_hits_add(self):
        """
        Test the add hits page
        """
        ret = self.flask_app.get("/test/addhits")
        assert ret.status_code == 200
        assert "submit" in ret.data

        ret = self.flask_app.post("/test/addhits", data=dict(
            datetime="2014-09-26T11:27:45",
            appid=1,
            hits=22
        ))
        assert ret.status_code == 302

        # Check that the hit was added successfully.
        s = sqla.db()
        hits = s.query(Hits).all()
        assert len(hits) == 1

        h = hits[0]
        assert h.hits == 22

    def test_apps_add(self):
        """
        Test the add apps page
        """
        ret = self.flask_app.get("/test/addapp")
        assert ret.status_code == 200
        assert "submit" in ret.data

        ret = self.flask_app.post("/test/addapp", data=dict(
            name="Test App",
            description="Description"
        ))
        assert ret.status_code == 302

        # Check that the hit was added successfully.
        s = sqla.db()
        apps = s.query(Application).all()
        names = [app.name for app in apps]
        assert "Test App" in names 

