from billing.billing_3scale import ThreescaleBilling, create_application
import config


class Test3Scale:
    def __init__(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nothing(self):
        pass

    def test_instance(self):
        api = ThreescaleBilling(config.THREESCALE_PROVIDER_KEY, config.THREESCALE_USER_KEY)
        assert api is not None

    def test_report_hits(self):
        api = ThreescaleBilling(config.THREESCALE_PROVIDER_KEY, config.THREESCALE_USER_KEY)
        api.report_hits(5)

    def test_report_time(self):
        api = ThreescaleBilling(config.THREESCALE_PROVIDER_KEY, config.THREESCALE_USER_KEY)
        api.report_time(20)

    def test_create_application(self):
        app = create_application(config.THREESCALE_ADMIN_SERVER, config.THREESCALE_PROVIDER_KEY, config.THREESCALE_ACCOUNT_ID, config.THREESCALE_PLAN_ID, "Test App", "Test App Description")
        assert app is not None