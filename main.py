


# Report usage with ThreeScale
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from billing import Billing
from billing_3scale import ThreescaleBilling
from billing_sqla import SqlaBilling
from config import *
from models import Base, User


strat = ThreescaleBilling(threescale_provider_key, threescale_user_key)
billing = Billing(strat)


billing.report_hits(1)
billing.report_time(30)




engine = create_engine('sqlite:///database.db')
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

