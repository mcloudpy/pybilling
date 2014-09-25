


# Report usage with ThreeScale
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from billing.billing import Billing
from billing.billing_3scale import ThreescaleBilling
from billing.billing_sqla import SqlaBilling
from billing.models import Base, Application

import config


strat = ThreescaleBilling(config.threescale_provider_key, config.threescale_user_key)
billing = Billing(strat)


billing.report_hits(1)
billing.report_time(30)




engine = create_engine(config.DATABASE_URI)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user = Application(name="TestUser")
session.add(user)
session.commit()
id = user.id
print id

strat = SqlaBilling(config.DATABASE_URI, id)
billing = Billing(strat)

billing.report_hits(1)
billing.report_time(30)

