import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from billing.models import Base, Hits, Application
from billingweb import flask_app as app
from billingweb import sqla
from billingweb.ajax_hits import accumulate_hits


class TestAjax:
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

    def test_accumulate_hits_monthly(self):
        """
        Test that the accumulate hits function works as expected for monthly hits.
        """
        ts1 = datetime.datetime(year=2014, month=2, day=1)
        ts2 = datetime.datetime(year=2014, month=2, day=2)
        ts3 = datetime.datetime(year=2014, month=3, day=2)

        original_hits = [
            Hits(ts=ts1, hits=5, app_id=2),
            Hits(ts=ts2, hits=6, app_id=2),
            Hits(ts=ts3, hits=8, app_id=2)
        ]

        # If using a monthly granularity, hits 1 and 2 should be accumulated, hits 2 not.

        accumulated = accumulate_hits(original_hits, "monthly")

        assert len(accumulated) == 2

        s = sorted(accumulated)

        h1 = accumulated[s[0]]
        h2 = accumulated[s[1]]

        assert h1.hits == 11  # 5+6
        assert h2.hits == 8

    def test_accumulate_hits_yearly(self):
        """
        Test that the accumulate hits function works as expected for monthly hits.
        """
        ts1 = datetime.datetime(year=2014, month=5, day=1)
        ts2 = datetime.datetime(year=2013, month=2, day=2)
        ts3 = datetime.datetime(year=2014, month=3, day=2)

        original_hits = [
            Hits(ts=ts1, hits=5, app_id=2),
            Hits(ts=ts2, hits=6, app_id=2),
            Hits(ts=ts3, hits=8, app_id=2)
        ]

        # If using a yearly granularity, hits 1 and 3 should be accumulated, hits 2 not.

        accumulated = accumulate_hits(original_hits, "yearly")

        assert len(accumulated) == 2

        s = sorted(accumulated)

        h1 = accumulated[s[0]]
        h2 = accumulated[s[1]]

        assert h1.hits == 6  # 5+6
        assert h2.hits == 13   

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




