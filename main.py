


# Report usage with ThreeScale
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from billing import Billing
from billing_3scale import ThreescaleBilling
from billing_sqla import SqlaBilling
from models import Base, User

import config


strat = ThreescaleBilling(config.threescale_provider_key, config.threescale_user_key)
billing = Billing(strat)


billing.report_hits(1)
billing.report_time(30)




engine = create_engine(config.DATABASE_URI)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user = User(name="TestUser")
session.add(user)
session.commit()
id = user.id
print id

strat = SqlaBilling(id)
billing = Billing(strat)

billing.report_hits(1)
billing.report_time(30)

