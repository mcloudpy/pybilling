import requests
from billing import BillingException


class ThreescaleBilling(object):

    DOMAIN_SERVER = "http://su1.3scale.net"

    def __init__(self, provider_key, user_key):
        self._provider_key = provider_key
        self._user_key = user_key

    def report_hits(self, hits):
        if hits < 0:
            raise BillingException("Error. Reported hits must be a positive integer.")
        ret = requests.get("%s/transactions/authrep.xml" % ThreescaleBilling.DOMAIN_SERVER, params=dict(
            {"usage[hits]": hits},
            provider_key=self._provider_key,
            user_key=self._user_key,
        ))
        if ret.status_code != 200:
            raise BillingException("Error reporting hits. Code: %s. Reason: %s" % (ret.status_code, ret.text))

    def report_time(self, time):
        if time < 0:
            raise BillingException("Error. Reported time must be a positive integer.")
        ret = requests.get("%s/transactions/authrep.xml" % ThreescaleBilling.DOMAIN_SERVER, params=dict(
            {"usage[time]": time},
            provider_key=self._provider_key,
            user_key=self._user_key
        ))
        if ret.status_code != 200:
            raise BillingException("Error reporting time. Code: %s. Reason: %s" % (ret.status_code, ret.text))