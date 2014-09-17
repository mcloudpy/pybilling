


# Report usage with ThreeScale
from billing import Billing
from billing_3scale import ThreescaleBilling
from config import *


strat = ThreescaleBilling(threescale_provider_key, threescale_user_key)
billing = Billing(strat)


billing.report_hits(1)
billing.report_time(30)