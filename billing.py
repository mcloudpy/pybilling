

class BillingException(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class Billing(object):

    def __init__(self, billing_strategy):
        self._strat = billing_strategy

    def report_hits(self, hits):
        self._strat.report_hits(hits)

    def report_time(self, time):
        self._strat.report_time(time)