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
        api = ThreescaleBilling(config.threescale_provider_key, config.threescale_user_key)
        assert api is not None

    def test_report_hits(self):
        api = ThreescaleBilling(config.threescale_provider_key, config.threescale_user_key)
        api.report_hits(5)

    def test_report_time(self):
        api = ThreescaleBilling(config.threescale_provider_key, config.threescale_user_key)
        api.report_time(20)

    def test_create_application(self):
        app = create_application(config.threescale_admin_server, config.threescale_provider_key, config.threescale_account_id, config.threescale_plan_id, "Test App", "Test App Description")
        assert app is not None