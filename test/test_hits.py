from run_web import app


class TestHits:
    def __init__(self):
        self.flask_app = None

    def setUp(self):
        self.flask_app = app.test_client()

    def tearDown(self):
        pass

    def test_nothing(self):
        pass

    def test_index(self):
        ret = self.flask_app.get("/")
        assert ret.status_code == 200

    def test_basic_hits(self):
        ret = self.flask_app.get("/")