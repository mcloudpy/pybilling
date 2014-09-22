# Initialize SQLAlchemy
from sqlalchemy.orm import sessionmaker
from billing.models import Base
from sqlalchemy import create_engine

import config

_db_eng = create_engine(config.DATABASE_URI)
Base.metadata.bind = _db_eng
db = sessionmaker(bind=_db_eng)