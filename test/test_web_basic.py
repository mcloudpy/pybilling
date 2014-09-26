import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from billing.models import Base
from billingweb import flask_app as app
from billingweb import sqla


class TestWebBasic:
    def __init__(self):
        self.flask_app = None

    def setUp(self):
        # Redirect SQLA to the test database.
        sqla._db_eng = create_engine("sqlite:///test_database.db")
        Base.metadata.bind = sqla._db_eng
        sqla.db = sessionmaker(bind=sqla._db_eng)

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

    def test_index_install_redirect(self):
        pass

    def test_install_get(self):
        """
        Test the Install's GET
        """
        ret = self.flask_app.get("/install")
        assert ret.status_code == 200
        assert "install" in ret.data
        assert "submit" in ret.data
        assert "<form" in ret.data

    def test_install_post(self):
        """
        Test the Install's POST
        """

        # Ensure the DB doesnt exist yet.
        assert not os.path.isfile("test_database.db")

        ret = self.flask_app.post("/install")

        assert os.path.isfile("test_database.db")

        # Ensure the DB seems to contain the valid tables.
        sqla._db_eng.execute("SELECT 1 FROM Application")


