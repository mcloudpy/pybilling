import ThreeScalePY
from billing import BillingException


class ThreescaleBilling(object):

    def __init__(self, provider_key, user_key):
        self._provider_key = provider_key
        self._user_key = user_key
        self._client = ThreeScalePY.ThreeScaleAuthRepUserKey(self._provider_key)

    def report_hits(self, hits):
        result = self._client.authrep(self._user_key, usage={"hits": hits})
        if not result:
            # Something failed.
            raise BillingException(self._client.build_response().get_reason())

    def report_time(self, time):
        result = self._client.authrep(self._user_key, usage={"time": time})
        if not result:
            # Something failed.
            raise BillingException(self._client.build_response().get_reason())